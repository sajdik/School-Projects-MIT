-- Project: FLP 1 - simplify-bkg   
-- Author: Ondrej Sajdik (xsajdi01)
-- Year: 2021

module ParseInput where
import Types
import Data.Char
import Data.Maybe
import Helper

-- Check input for size and format
checkInput :: String -> Bool
checkInput input = checkSize input && checkFormat input

-- Check input if it has expected minimum amount of lines
checkSize :: String -> Bool
checkSize str = length (lines str) >= 3

-- Check input format defining BKG
checkFormat :: String -> Bool
checkFormat str = check isUpper nonTerminals && check isLower terminals &&
              check isUpper startingSymbol && length startingSymbol == 1 
              && check ruleFormat rules
    where
        nonTerminals = rmAllOccurrences (head lineList) ',' 
        terminals = rmAllOccurrences (lineList !! 1) ','
        startingSymbol = lineList !! 2
        rules = drop 3 lineList
        lineList = lines str

-- Check list of values by specified function and unify result
check:: (a -> Bool) -> [a] -> Bool
check f = foldr ((&&) . f) True

-- Check format of single rule
ruleFormat :: String -> Bool
ruleFormat rule
    | null rule = True
    | otherwise = length rule >= 4 && isUpper (head rule) && check isAlp (drop 3 rule)

-- Check  weather char is alphabet + #
isAlp :: Char -> Bool
isAlp x = x `elem` ('#':['a'..'z'] ++ ['A'..'Z'])

-- Convert string  into Grammar
parse :: String -> Grammar
parse str = Grammar (rmDuplicates (parseSymbols (head lineList))) 
    (rmDuplicates (parseSymbols (lineList !! 1))) 
    (parseStart (lineList !! 2)) 
    (parseRules (filter (not . null) (drop 3 lineList)))
    where lineList = lines str

-- Parse symbols (removing ',' from string)
parseSymbols :: String -> [Char]
parseSymbols str = rmAllOccurrences str ','

-- Parse start symbol
parseStart :: String -> Char
parseStart = head

-- Parse rules
-- Input: lines with rules
-- Output: list of rules
parseRules :: [String] -> [Rule]
parseRules = map parseRule

-- Parse single rule
parseRule :: String -> Rule
parseRule str = Rule (head str, drop 3 str)
