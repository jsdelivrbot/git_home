{-# LANGUAGE OverloadedStrings #-}
{-# LANGUAGE RecordWildCards #-}

module KaggleTerror 
  ( Item(..)
  )
  where
-- base
import Control.Exception (IOException)
import qualified Control.Exception as Exception
import qualified Data.Foldable as Foldable

-- bytestring
import Data.ByteString.Lazy (ByteString)
import qualified Data.ByteString.Lazy as ByteString

-- cassava
import Data.Csv
  ( DefaultOrdered(headerOrder)
  , FromField(parseField)
  , FromNamedRecord(parseNamedRecord)
  , Header
  , ToField(toField)
  , ToNamedRecord(toNamedRecord)
  , (.:)
  , (.=)
  )
import qualified Data.Csv as Cassava

-- text
import Data.Text (Text)
import qualified Data.Text.Encoding as Text

-- vector
import Data.Vector (Vector)
import qualified Data.Vector as Vector

import Data.Maybe

data Item = 
  Item
    { year :: Int
    , month :: Int
    , day :: Int
    , city :: Text
    , country :: Int
    , region :: Int
    , provstate :: Text
    , nkill :: Maybe Int
    , nkillter :: Maybe Int
    }
    deriving (Eq, Show)

sample_item :: Item
sample_item =
  Item
    { year = 1988
    , month = 8
    , day = 19
    , city = "Lisnaskea"
    , country = 603
    , region = 8
    , provstate = "Northen Ireland"
    , nkill = Just 0
    , nkillter = Nothing
    }
