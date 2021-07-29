-- Project: FLP 1 - simplify-bkg   
-- Author: Ondrej Sajdik (xsajdi01)
-- Year: 2021

module Helper where 

import Types ( Rule(..), Grammar(..) )

-- Removes duplicate chars in char list
rmDuplicates :: [Char] -> [Char]
rmDuplicates str
    | null str = []
    | otherwise = head str : rmDuplicates (rmAllOccurrences (tail str) (head str)) 

-- Removes all occurrences of char x in string str
-- Input: string str, char x to be removed
-- Output: string with no occurrences of x
rmAllOccurrences :: String -> Char -> String
rmAllOccurrences str x
    | null str = []
    | head str == x = rmAllOccurrences (tail str) x
    | otherwise = head str : rmAllOccurrences(tail str) x

-- PRINT FUNCTIONS 
-- Functions converting grammar to string

-- Convert grammar to string 
gToStr :: Grammar -> String
gToStr (Grammar nt t s r) = termToStr nt ++ termToStr t ++ [s] ++ "\n" ++ concatMap rToStr r

-- Convert rule to string
rToStr :: Rule -> String
rToStr (Rule (from, to)) = from : "->" ++ to ++ "\n"

-- Convert list of terms to string
termToStr :: String -> String
termToStr nt
    | null nt = "\n"
    | otherwise = head nt : nextTermToStr (tail nt)

nextTermToStr :: String -> String
nextTermToStr nt
    | null nt = "\n"
    | otherwise = ',' : head nt : nextTermToStr (tail nt)