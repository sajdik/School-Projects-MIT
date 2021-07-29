-- Project: FLP 1 - simplify-bkg   
-- Author: Ondrej Sajdik (xsajdi01)
-- Year: 2021

module Simplify where
import Types
import Data.List
import Data.Char
import Helper

--- Step 1 of removing useless symbols.

-- Remove non-terminals generating no strings and rules using them
-- Input: Context-free Grammar 
-- Output: Context-free Grammar without non-generating symbols 
step1 :: Grammar -> Grammar
step1 (Grammar nT t s r) = Grammar (rmDuplicates (s:nt)) t s (removeRules r (nt++t))
    where nt = buildNt nT t r []

-- Build list of non-terminals generating terminal symbols using rules
-- Input: non-terminals, terminals, rules ,(new list of non-terminals)
-- Output: new list of non-terminals generating terminal symbols
buildNt :: [Char] -> [Char] -> [Rule] -> [Char] -> [Char]
buildNt nonTerms terms rules nt
    | nt == ntNext  = ntNext
    | otherwise     = buildNt nonTerms terms rules ntNext
    where ntNext = nextNt nonTerms rules (terms ++ nt)

-- {A | A → α in P ∧ α ∈ (Ni−1 ∪ Σ)∗}
-- Input: non-terminals, rules, α(non-terminals+terminals)
-- Output: new-list of non terminals generating string made from α*
nextNt :: [Char] -> [Rule] -> [Char] -> [Char]
nextNt nonTerms rules alpha = [n | n <- nonTerms, existRule rules n alpha ]

-- Check if non-terminal generates alpha
-- Input: list of rules, non-terminal, α(non-terminals+terminals)
-- Output: True if non-terminal generates string from α* using rules, Otherwise False
existRule :: [Rule] -> Char -> [Char] -> Bool
existRule rules n alpha = not (null [rule | rule <- rules, (from rule == n) 
                            && compareWithIteration (to rule) alpha])

-- Check if string is made using only chars from alpha
-- Input: string to be checked, list of chars alpha
-- Output: True if string is subset of alpha*
compareWithIteration :: String -> [Char] -> Bool
compareWithIteration str alpha
    | null str      = True
    | head str `elem` alpha = compareWithIteration (tail str) alpha
    | otherwise = False

--- Step 2 of removing useless symbols.

-- Remove unreachable terminals, non-terminals and rules using them 
-- Input: Context-free Grammar 
-- Output: Context-free Grammar without unreachable symbols
step2 :: Grammar -> Grammar
step2 (Grammar nt t s r) = 
    Grammar (rmDuplicates (s : nt `intersect` v)) (t `intersect` v) s (removeRules r v)
    where v = buildV (nt++t) r [s]

-- Iteratively build list of reachable symbols
-- Input: list of symbols, list of rules, list of reachable symbols
-- Vi= {X | A→αXβ ∈ P ∧ A ∈ Vi−1} ∪ Vi−1
buildV :: [Char] -> [Rule] -> [Char] -> [Char]
buildV symbols rules v
    | v == vNext    = vNext
    | otherwise     = buildV symbols rules vNext
    where vNext = nextV symbols rules v

-- Build list of reachable symbols
-- Input: list of symbols, list of rules, list of reachable symbols
-- Output: list of reachable symbols
nextV :: [Char] -> [Rule] -> [Char] -> [Char]
nextV symbols rules v = rmDuplicates ( [n | n <- symbols, isGenerated rules v n] ++ v )

-- Check if symbol x is generated from any symbol of symbols list
-- Input: list of rules, list of reachable symbols, symbol x
-- Output: True if exists rule generating x from any of reachable symbols
isGenerated :: [Rule] -> [Char] -> Char -> Bool
isGenerated rules symbols x = 
    not (null ([rule | rule <- rules, from rule `elem` symbols && x `elem` to rule]))

-- Remove rules not using symbols
-- Input: list of rules, list of symbols symbols
-- Output: list of rules using only non-terminals from nt list
removeRules :: [Rule] -> [Char] -> [Rule]
removeRules rules symbols = 
    [rule | rule <- rules, 
        from rule `elem` symbols && ([x | x <- to rule, x `elem` symbols || x == '#'] == to rule)
    ]

