-- Project: FLP 1 - simplify-bkg   
-- Author: Ondrej Sajdik (xsajdi01)
-- Year: 2021

module Types where

-- Rule from->to
newtype Rule = Rule (Char, String)

from :: Rule -> Char
from (Rule (x, _)) = x
to :: Rule -> String
to (Rule (_, x)) = x

-- Context-free grammar 
data Grammar = Grammar String  String Char [Rule]