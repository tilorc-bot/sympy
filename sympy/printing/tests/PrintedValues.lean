/-!
Used by `lean_values` in check_printed_code.py, after `import Mathlib`.

Evaluate an elaborated real-valued Lean term at points, with `Float`s, by
reading Mathlib's definitions off the term: `Real.sin` is `Float.sin`, and
the junk values of Mathlib's total functions are reproduced (`x / 0 = 0`,
`Real.log x = log |x|`, `Real.sqrt x = 0` for `x < 0`, ...). `deriv`,
`iteratedDeriv 2` and integrals are approximated numerically. A function,
constant or instance it doesn't know is an error, never a guess.
-/

open Lean Meta Elab Command

namespace PrintedEval

inductive V where
  | r : Float → V          -- a real number
  | i : Int → V            -- an integer or natural number
  | b : Bool → V           -- a proposition (decided)
  | lam : List V → Expr → V  -- a function: its context and body

def V.real : V → MetaM Float
  | .r x => pure x
  | .i n => pure (Float.ofInt n)
  | _ => throwError "not a number"

def V.int : V → MetaM Int
  | .i n => pure n
  | _ => throwError "not an integer"

def V.bool : V → MetaM Bool
  | .b p => pure p
  | _ => throwError "not a proposition"

def pi : Float := 3.141592653589793

/-- What Mathlib's `Real.log` is: `log |x|`, and `0` at `0` -/
def rlog (x : Float) : Float := if x == 0 then 0 else Float.log x.abs

def rdiv (x y : Float) : Float := if y == 0 then 0 else x / y

/-- `Real.rpow`: `exp (log x * y)` for `x > 0`, `0 ^ y = 0` unless `y = 0`,
and `exp (log |x| * y) * cos (y * π)` for `x < 0` -/
def rpow (x y : Float) : Float :=
  if x == 0 then (if y == 0 then 1 else 0)
  else if x > 0 then Float.exp (Float.log x * y)
  else Float.exp (Float.log (-x) * y) * Float.cos (y * pi)

def zpow (x : Float) (n : Int) : Float :=
  if n ≥ 0 then x ^ Float.ofInt n else rdiv 1 (x ^ Float.ofInt (-n))

def isType (t : Expr) (n : Name) : Bool := t.consumeMData.isConstOf n

def rsqrt (x : Float) : Float := if x < 0 then 0 else Float.sqrt x

/-- `Real.Gamma`: the Lanczos approximation (g = 7), and `0` at the poles
`0, -1, -2, ...` as in Mathlib -/
partial def gamma (x : Float) : Float :=
  if x ≤ 0 && x == x.floor then 0
  else if x < 0.5 then pi / (Float.sin (pi * x) * gamma (1 - x))
  else
    let c := #[0.99999999999980993, 676.5203681218851, -1259.1392167224028,
      771.32342877765313, -176.61502916214059, 12.507343278686905,
      -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]
    let x := x - 1
    let t := x + 7.5
    let a := (List.range 8).foldl (fun a k => a + c.getD (k + 1) 0 / (x + (k + 1).toFloat)) (c.getD 0 0)
    Float.sqrt (2 * pi) * t ^ (x + 0.5) * Float.exp (-t) * a

def realFns : List (Name × (Float → Float)) := [
  (``Real.exp, Float.exp), (``Real.log, rlog),
  (``Real.sqrt, rsqrt),
  (``Real.sin, Float.sin), (``Real.cos, Float.cos),
  (``Real.tan, fun x => rdiv (Float.sin x) (Float.cos x)),
  (``Real.cot, fun x => rdiv (Float.cos x) (Float.sin x)),
  (``Real.arcsin, fun x => if x ≥ 1 then pi / 2 else if x ≤ -1 then -pi / 2 else Float.asin x),
  (``Real.arccos, fun x => if x ≥ 1 then 0 else if x ≤ -1 then pi else Float.acos x),
  (``Real.arctan, Float.atan),
  (``Real.sinh, Float.sinh), (``Real.cosh, Float.cosh), (``Real.tanh, Float.tanh),
  (``Real.arsinh, Float.asinh),
  -- Mathlib's definitions, with its total log, √ and /
  (``Real.arcosh, fun x => rlog (x + rsqrt (x ^ 2 - 1))),
  (``Real.artanh, fun x => rlog (rsqrt (rdiv (1 + x) (1 - x)))),
  (``Real.Gamma, gamma),
  (``Real.sign, fun x => if x > 0 then 1 else if x < 0 then -1 else 0)]

/-- Integrate f from a to b: composite 5-point Gauss–Legendre, 64 panels -/
def integrate (f : Float → MetaM Float) (a b : Float) : MetaM Float := do
  let nodes := #[(0.0, 0.5688888888888889), (-0.5384693101056831, 0.4786286704993665),
    (0.5384693101056831, 0.4786286704993665), (-0.9061798459386640, 0.2369268850561891),
    (0.9061798459386640, 0.2369268850561891)]
  let n := 64
  let h := (b - a) / n.toFloat
  let mut s := 0.0
  for k in [0:n] do
    let m := a + (k.toFloat + 0.5) * h
    for (t, w) in nodes do
      s := s + w * (← f (m + t * h / 2))
  return s * h / 2

mutual

partial def apply (f : V) (args : List V) : MetaM V := do
  match f, args with
  | f, [] => pure f
  | .lam ctx body, a :: rest => apply (← ev (a :: ctx) body) rest
  | _, _ => throwError "applying a value that isn't a function"

partial def realFn (ctx : List V) (f : Expr) : MetaM (Float → MetaM Float) := do
  let fv ← ev ctx f
  return fun x => do (← apply fv [.r x]).real

partial def ev (ctx : List V) (e : Expr) : MetaM V := do
  match e with
  | .mdata _ e => ev ctx e
  | .bvar k => match ctx[k]? with
    | some v => pure v
    | none => throwError "unbound variable"
  | .lit (.natVal n) => pure (.i n)
  | .lam _ _ body _ => pure (.lam ctx body)
  | .letE _ _ v b _ => ev ((← ev ctx v) :: ctx) b
  | .forallE _ p q _ =>   -- p → q
    if q.hasLooseBVars then throwError "can't evaluate a ∀"
    else pure (.b (!(← (← ev ctx p).bool) || (← (← ev ctx q).bool)))
  | _ =>
  let fn := e.getAppFn
  let args := e.getAppArgs
  if fn.isLambda || fn.isBVar then
    return ← apply (← ev ctx fn) (← args.toList.mapM (ev ctx))
  let .const name _ := fn | throwError "can't evaluate {e}"
  let arg (k : Nat) : MetaM V := ev ctx args[k]!
  let real (k : Nat) : MetaM Float := do (← arg k).real
  match name, args.size with
  | ``Real.pi, 0 => return .r pi
  | ``Real.goldenRatio, 0 => return .r ((1 + Float.sqrt 5) / 2)
  | ``Real.eulerMascheroniConstant, 0 => return .r 0.5772156649015329
  | ``True, 0 => return .b true
  | ``False, 0 => return .b false
  | ``OfNat.ofNat, 3 =>
    let n ← (← arg 1).int
    if isType args[0]! ``Real then return .r (Float.ofInt n)
    if isType args[0]! ``Int || isType args[0]! ``Nat then return .i n
    throwError "a numeral of type {args[0]!}"
  | ``OfScientific.ofScientific, 5 =>
    unless isType args[0]! ``Real do throwError "a decimal that isn't real"
    let m ← (← arg 2).int
    let .const s _ := args[3]!.consumeMData | throwError "a decimal"
    let ex ← (← arg 4).int
    return .r (Float.ofScientific m.toNat (s == ``Bool.true) ex.toNat)
  | ``Int.cast, 3 | ``IntCast.intCast, 3 | ``Nat.cast, 3 | ``NatCast.natCast, 3 =>
    unless isType args[0]! ``Real do throwError "a cast to {args[0]!}"
    return .r (Float.ofInt (← (← arg 2).int))
  | ``HAdd.hAdd, 6 | ``HSub.hSub, 6 | ``HMul.hMul, 6 | ``HDiv.hDiv, 6 =>
    let t := args[0]!
    if !(isType t ``Real) then
      unless (isType t ``Int || isType t ``Nat) && name != ``HDiv.hDiv do
        throwError "{name} on {t}"
      let a ← (← arg 4).int
      let b ← (← arg 5).int
      return .i (match name with
        | ``HAdd.hAdd => a + b | ``HSub.hSub => if isType t ``Nat then (a - b).toNat else a - b
        | _ => a * b)
    let a ← real 4
    let b ← real 5
    return .r (match name with
      | ``HAdd.hAdd => a + b | ``HSub.hSub => a - b | ``HMul.hMul => a * b
      | _ => rdiv a b)
  | ``Neg.neg, 3 =>
    if isType args[0]! ``Real then return .r (-(← real 2))
    if isType args[0]! ``Int then return .i (-(← (← arg 2).int))
    throwError "Neg on {args[0]!}"
  | ``Inv.inv, 3 =>
    unless isType args[0]! ``Real do throwError "Inv on {args[0]!}"
    return .r (rdiv 1 (← real 2))
  | ``HPow.hPow, 6 =>
    let base := args[0]!
    let ex := args[1]!
    if isType base ``Real then
      let x ← real 4
      if isType ex ``Nat || isType ex ``Int then return .r (zpow x (← (← arg 5).int))
      if isType ex ``Real then return .r (rpow x (← real 5))
    if isType base ``Int && isType ex ``Nat then
      return .i ((← (← arg 4).int) ^ (← (← arg 5).int).toNat)
    throwError "a power {base} ^ {ex}"
  | ``abs, k + 1 =>
    if isType args[0]! ``Real then return .r (← real k).abs
    if isType args[0]! ``Int then return .i (← (← arg k).int).natAbs
    throwError "abs on {args[0]!}"
  | ``Int.floor, k + 1 | ``Int.ceil, k + 1 =>
    unless isType args[0]! ``Real do throwError "floor on {args[0]!}"
    let x ← real k
    let y := if name == ``Int.floor then x.floor else x.ceil
    unless y.abs < 1e15 do throwError "floor of a number too large for a Float"
    return .i y.toInt64.toInt
  | ``Max.max, 4 | ``Min.min, 4 =>
    unless isType args[0]! ``Real do throwError "max on {args[0]!}"
    let a ← real 2
    let b ← real 3
    return .r (if name == ``Max.max then (if a ≥ b then a else b) else (if a ≤ b then a else b))
  | ``Complex.arg, 1 =>
    let z := args[0]!.consumeMData
    unless z.isAppOfArity ``Complex.mk 2 do throwError "arg of a complex number"
    let x ← (← ev ctx (z.getArg! 0)).real
    let y ← (← ev ctx (z.getArg! 1)).real
    return .r (Float.atan2 y x)
  | ``ite, 5 =>
    if ← (← arg 1).bool then arg 3 else arg 4
  | ``LT.lt, 4 | ``LE.le, 4 | ``GT.gt, 4 | ``GE.ge, 4 =>
    unless isType args[0]! ``Real || isType args[0]! ``Int do throwError "order on {args[0]!}"
    let a ← (← arg 2).real
    let b ← (← arg 3).real
    return .b (match name with
      | ``LT.lt => a < b | ``LE.le => a ≤ b | ``GT.gt => a > b | _ => a ≥ b)
  | ``Eq, 3 => return .b ((← (← arg 1).real) == (← (← arg 2).real))
  | ``Ne, 3 => return .b ((← (← arg 1).real) != (← (← arg 2).real))
  | ``And, 2 => return .b ((← (← arg 0).bool) && (← (← arg 1).bool))
  | ``Or, 2 => return .b ((← (← arg 0).bool) || (← (← arg 1).bool))
  | ``Not, 1 => return .b !(← (← arg 0).bool)
  | ``Iff, 2 => return .b ((← (← arg 0).bool) == (← (← arg 1).bool))
  | ``deriv, k + 2 =>
    unless isType args[0]! ``Real && isType args[2]! ``Real do throwError "deriv over {args[0]!}"
    let f ← realFn ctx args[k]!
    let x ← real (k + 1)
    -- central differences with Richardson extrapolation
    let h := 1e-3 * (if x.abs > 1 then x.abs else 1)
    let d (h : Float) : MetaM Float := do return ((← f (x + h)) - (← f (x - h))) / (2 * h)
    let d1 ← d h
    let d2 ← d (h / 2)
    let d3 ← d (h / 4)
    let r1 := (4 * d2 - d1) / 3
    let r2 := (4 * d3 - d2) / 3
    return .r ((16 * r2 - r1) / 15)
  | ``iteratedDeriv, k + 3 =>
    unless isType args[0]! ``Real && isType args[2]! ``Real do throwError "deriv over {args[0]!}"
    let n ← (← arg k).int
    unless n == 2 do throwError "iteratedDeriv {n}"
    let f ← realFn ctx args[k + 1]!
    let x ← real (k + 2)
    let h := 1e-3 * (if x.abs > 1 then x.abs else 1)
    let d (h : Float) : MetaM Float := do
      return ((← f (x + h)) - 2 * (← f x) + (← f (x - h))) / (h * h)
    let d1 ← d h
    let d2 ← d (h / 2)
    return .r ((4 * d2 - d1) / 3)
  | ``Finset.sum, 5 | ``Finset.prod, 5 =>
    unless isType args[1]! ``Real do throwError "sum of {args[1]!}"
    let s := args[3]!.consumeMData
    unless s.isAppOfArity ``Finset.Icc 5 && isType (s.getArg! 0) ``Int do
      throwError "a sum over {s}"
    let lo ← (← ev ctx (s.getArg! 3)).int
    let hi ← (← ev ctx (s.getArg! 4)).int
    unless hi - lo < 100000 do throwError "a sum of too many terms"
    let f ← ev ctx args[4]!
    let mut acc : Float := if name == ``Finset.sum then 0 else 1
    let mut k := lo
    while k ≤ hi do
      let v ← (← apply f [.i k]).real
      acc := if name == ``Finset.sum then acc + v else acc * v
      k := k + 1
    return .r acc
  | ``intervalIntegral, k + 4 =>
    unless isType args[0]! ``Real do throwError "an integral of {args[0]!}"
    let f ← realFn ctx args[k]!
    return .r (← integrate f (← real (k + 1)) (← real (k + 2)))
  | _, 1 =>
    match realFns.lookup name with
    | some g => return .r (g (← real 0))
    | none => throwError "can't evaluate {name}"
  | _, _ => throwError "can't evaluate {name} with {args.size} arguments"

end

/-- `#printed_values f at [[x₁, y₁], ...]`: the values of the function `f` of
real and integer arguments at the points, as a list of the bits of each
`Float`, `null` for NaN or ±∞, or why it can't be evaluated -/
elab "#printed_values " f:term " at " pts:term : command => liftTermElabM do
  let f ← Term.elabTerm f none
  Term.synthesizeSyntheticMVarsNoPostponing
  let f ← instantiateMVars f
  let pts ← Term.elabTerm pts (some (mkApp (mkConst ``List [.zero]) (mkApp (mkConst ``List [.zero]) (mkConst ``Float))))
  Term.synthesizeSyntheticMVarsNoPostponing
  let pts ← instantiateMVars pts
  let pts ← unsafe evalExpr (List (List Float)) (mkApp (mkConst ``List [.zero]) (mkApp (mkConst ``List [.zero]) (mkConst ``Float))) pts
  -- the binder types decide whether an argument is real or an integer
  let types ← lambdaTelescope f fun xs _ => xs.toList.mapM fun x => do return (← inferType x)
  let mut out := #[]
  for p in pts do
    let args := (types.zip p).map fun (t, x) =>
      if isType t ``Int then V.i x.round.toInt64.toInt else V.r x
    try
      let v ← apply (← ev [] f) args
      let x ← v.real
      out := out.push (if x.isNaN || x.isInf then "null" else toString x.toBits.toNat)
    catch err =>
      out := out.push s!"\"{(← err.toMessageData.toString).replace "\"" "'" |>.replace "\n" " "}\""
  logInfo m!"[{", ".intercalate out.toList}]"

end PrintedEval
