-- Project: FLP 1 - simplify-bkg   
-- Author: Ondrej Sajdik (xsajdi01)
-- Year: 2021

import System.IO (hPutStrLn, stderr)
import System.Environment ( getArgs )
import Types ( Grammar(..), Rule(..) )
import Simplify ( step1, step2 )
import ParseInput ( parse, checkInput )
import Helper ( gToStr )
import Data.Char ()

-- MAIN
main :: IO ()
main = do
    args <- getArgs

    let fileName = getFile args
    input <- if fileName == "" then getContents else readFile fileName
    -- Grammar read from input
    let g0 = parse input

    -- Grammar after 1. step of algorithm
    let g1 = step1 g0

    -- Grammar after 2. step of algorithm
    let g2 = step2 g1

    if checkInput input 
        then putStr (gToStr(chooseResult args g0 g1 g2)) 
        else hPutStrLn stderr "Error: unexpected input"

-- Extract filename from program arguments
-- Input: List of arguments 
-- Output: Filename if found. Otherwise empty string.
getFile :: [String] -> String
getFile args
    | null files = ""
    | otherwise  =  head files
    where files = [x | x <- args, x `notElem` ["-i", "-1", "-2"]]

-- Chooses grammar based on arguments
-- Input: List of arguments, 3 grammars
-- Output: Chosen grammar based on arguments
chooseResult :: [String] -> Grammar -> Grammar -> Grammar -> Grammar
chooseResult args g0 g1 g2
    | "-i" `elem` args = g0
    | "-1" `elem` args = g1
    | "-2" `elem` args = g2
    | otherwise  = g2


