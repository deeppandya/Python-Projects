module Main where

import System.IO
import Control.Monad
import Data.List as L
import Data.List.Split
import qualified Data.Map as Map
import Data.Maybe
import Text.Printf

main::IO()
main = do
        cfile <- readFile "CustDB.slc"
        let clines = lines cfile
        let clist = getcust clines []
        sfile <- readFile "SalesDB.slc"
        let slines = lines sfile
        let slist = getsales slines []
        ofile <- readFile "OrderDB.slc"
        let olines = lines ofile
        let olist = getorder olines []
        let result = Main.condense clist slist olist
        printf "%-16s%-8s%-10s%2s" "custr" "order" "date"   "num of items" 
        printf "\n"
        putStr . unlines $ concatMap  format_customer result       
        
        
getcust list newlist = 
        if L.null list == False
        then
                let l = head list in
                let id = (splitOn "|" l)!!0 in
                let custname = (splitOn "|" l)!!1 in
                let record = db_customer custname id in
                let tlist = record:newlist in
                getcust (tail list) tlist
        else newlist
       
getsales list newlist = 
        if L.null list == False
        then
                let l = head list in
                let oid = (splitOn "|" l)!!0 in
                let cid = (splitOn "|" l)!!1 in
                let date = (splitOn "|" l)!!2 in
                let record = dbSale oid cid date in
                let tlist = record:newlist in
                getsales (tail list) tlist
        else newlist
     
getorder list newlist = 
        if L.null list == False
        then
                let l = head list in
                let id = (splitOn "|" l)!!0 in
                let item = (splitOn "|" l)!!1 in
                let record = dbOrder id item in
                let tlist = record:newlist in
                getorder (tail list) tlist
        else newlist 


data _customer = _customer { _customerName :: String
                         , sales        :: [Sale]
                         } deriving (Eq, Read, Show)

data _sale = _sale { orderID :: String
                 , _saleDate  :: String
                 , soldItems :: [String]
                 } deriving (Eq, Read, Show)

data db_customer = db_customer { db_customerName :: String
                             , db_customerID   :: String
                             } deriving (Eq, Read, Show)

data db_sale = db_sale { _saleOrderID    :: String
                     , _sale_customerID :: String
                     , db_saleDate     :: String
                     } deriving (Eq, Read, Show)

data dbOrder = dbOrder { dbOrderID   :: String
                       , dbOrderItem :: String
                       } deriving (Eq, Read, Show)                       
                        
condense :: [db_customer] -> [db_sale] -> [dbOrder] -> [_customer]
condense db_customers db_sales dbOrders = flip map db_customers $ \db_customer ->
    _customer (db_customerName db_customer)
           $ lookupDef [] (db_customerID db_customer) _salesBy_customerID where
  lookupDef :: (Ord k) => a -> k -> Map.Map k a -> a
  lookupDef def = (fromMaybe def .) . Map.lookup
  _salesBy_customerID = Map.fromListWith (++) . flip map db_sales
                    $ \db_sale -> (_sale_customerID db_sale,
                                  [ _sale (_saleOrderID db_sale) (db_saleDate db_sale)
                                  $ lookupDef [] (_saleOrderID db_sale)
                                              ordersByID])
  ordersByID = Map.fromListWith (++) . flip map dbOrders
             $ \dbOrder -> (dbOrderID dbOrder, [dbOrderItem dbOrder])
             
format_sale :: _customer -> _sale -> String
format_sale _customer _sale = printf "%-16s%-8s%-10s%-10s"
                                  (_customerName _customer)
                                  (orderID _sale)
                                  (show $ _saleDate _sale)
                                  (intercalate "," $ soldItems _sale)             
format_customer :: _customer -> [String]
format_customer _customer = map (format_sale _customer) $ _sales _customer
                       
