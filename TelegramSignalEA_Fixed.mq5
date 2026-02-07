//+------------------------------------------------------------------+
//| TelegramSignalEA_Fixed.mq5                                       |
//| Fixed version with Grid Limits and SL Updates                    |
//+------------------------------------------------------------------+
#property copyright "Telegram Signal EA Fixed"
#property version "2.01"
#property strict

//+------------------------------------------------------------------+
//| Input Parameters                                                  |
//+------------------------------------------------------------------+
input group "=== SYMBOL MAPPING ==="
input bool AutoDetectGold = true;
input string ManualGoldSymbol = "";

input group "=== LOT SIZE SETTINGS ==="
enum LotMode { FIXED_LOTS, PERCENTAGE_RISK };
input LotMode LotSizeMode = FIXED_LOTS;
input double FixedLotSize = 0.01;
input double RiskPercentage = 1.0;
input int MaxTradesPerSignal = 10;

input group "=== TRADE SPACING ==="
input int PipGapBetweenTrades = 10;

input group "=== TAKE PROFIT DISTRIBUTION ==="
input double TP1_Percentage = 30.0;
input double TP2_Percentage = 30.0;
input double TP3_Percentage = 20.0;

input group "=== BREAKEVEN SETTINGS ==="
input int BreakevenPips = 5;

input group "=== FILE SETTINGS ==="
enum FileLocation { TERMINAL_COMMON, TERMINAL_DATA };
input FileLocation CSVLocation = TERMINAL_COMMON;
input string CSVFileName = "trade_signals.csv";

input group "=== EA IDENTIFICATION ==="
input int MagicNumber = 123456;

//+------------------------------------------------------------------+
//| Global Variables                                                  |
//+------------------------------------------------------------------+
string LastProcessedTimestamp = "";
datetime LastFileCheckTime = 0;
int FileCheckIntervalSeconds = 1;
double PointValue;
string CurrentSymbol;
string TradingSymbol;

string GoldVariants[] = {"XAUUSD", "XAUUSDm", "XAUUSD.", "XAUUSDc", "GOLD", "GOLDm"};
string SignalSymbols[] = {"XAUUSDm", "GOLD", "gold"};

//+------------------------------------------------------------------+
//| Expert initialization                                             |
//+------------------------------------------------------------------+
int OnInit()
{
   CurrentSymbol = Symbol();
   TradingSymbol = CurrentSymbol;
   
   if(AutoDetectGold)
   {
      if(IsGoldSymbol(CurrentSymbol))
      {
         TradingSymbol = CurrentSymbol;
         Print("✅ Auto-detected GOLD symbol: ", TradingSymbol);
      }
      else
      {
         string foundGold = FindGoldSymbolInMarketWatch();
         if(foundGold != "")
         {
            TradingSymbol = foundGold;
            Print("✅ Found GOLD in Market Watch: ", TradingSymbol);
         }
         else
         {
            Print("❌ No GOLD symbol found");
            return(INIT_FAILED);
         }
      }
   }
   else if(ManualGoldSymbol != "")
   {
      TradingSymbol = ManualGoldSymbol;
      Print("✅ Using manual GOLD symbol: ", TradingSymbol);
   }
   
   if(!SymbolSelect(TradingSymbol, true))
   {
      Print("❌ Symbol not found: ", TradingSymbol);
      return(INIT_FAILED);
   }
   
   PointValue = SymbolInfoDouble(TradingSymbol, SYMBOL_POINT);
   if(SymbolInfoInteger(TradingSymbol, SYMBOL_DIGITS) == 3 ||
      SymbolInfoInteger(TradingSymbol, SYMBOL_DIGITS) == 5)
   {
      PointValue *= 10;
   }
   
   Print("========================================");
   Print("=== Telegram Signal EA Fixed v2.1 Started ===");
   Print("Chart Symbol: ", CurrentSymbol);
   Print("Trading Symbol: ", TradingSymbol);
   Print("CSV Location: ", (CSVLocation == TERMINAL_COMMON ? "Common Folder" : "Terminal Data"));
   Print("CSV File: ", CSVFileName);
   Print("Magic Number: ", MagicNumber);
   Print("========================================");
   
   // Test CSV file access immediately
   TestCSVFile();
   
   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Test CSV file access on startup                                  |
//+------------------------------------------------------------------+
void TestCSVFile()
{
   string filePath = CSVFileName;
   int flags = FILE_READ | FILE_TXT | FILE_ANSI;
   if(CSVLocation == TERMINAL_COMMON) flags |= FILE_COMMON;
   
   Print("\n🔍 TESTING CSV FILE ACCESS...");
   
   if(!FileIsExist(CSVFileName, (CSVLocation == TERMINAL_COMMON ? FILE_COMMON : 0)))
   {
      Print("❌ CSV file NOT FOUND: ", CSVFileName);
      Print("⚠️ Please ensure Python script is running and has created the file");
      return;
   }
   
   Print("✅ CSV file exists!");
   
   int fileHandle = FileOpen(CSVFileName, flags);
   
   if(fileHandle == INVALID_HANDLE)
   {
      Print("❌ Cannot open CSV file. Error: ", GetLastError());
      return;
   }
   
   Print("✅ CSV file opened successfully!");
   
   // Read and display content
   int lineCount = 0;
   while(!FileIsEnding(fileHandle) && lineCount < 5)
   {
      string line = FileReadString(fileHandle);
      if(line != "")
      {
         Print("Line ", lineCount, ": ", line);
         lineCount++;
      }
   }
   
   FileClose(fileHandle);
   Print("📊 Total lines read: ", lineCount);
   Print("========================================\n");
}

void OnDeinit(const int reason)
{
   Print("=== EA Stopped ===");
}

void OnTick()
{
   if(TimeCurrent() - LastFileCheckTime >= FileCheckIntervalSeconds)
   {
      LastFileCheckTime = TimeCurrent();
      CheckForNewSignals();
   }
}

//+------------------------------------------------------------------+
//| Check CSV for new signals                                        |
//+------------------------------------------------------------------+
void CheckForNewSignals()
{
   int flags = FILE_READ | FILE_TXT | FILE_ANSI;
   if(CSVLocation == TERMINAL_COMMON) flags |= FILE_COMMON;
   
   if(!FileIsExist(CSVFileName, (CSVLocation == TERMINAL_COMMON ? FILE_COMMON : 0)))
   {
      return;
   }
   
   int fileHandle = FileOpen(CSVFileName, flags);
   
   if(fileHandle == INVALID_HANDLE)
   {
      return;
   }
   
   ProcessCSVFile(fileHandle);
   FileClose(fileHandle);
}

//+------------------------------------------------------------------+
//| Process CSV file                                                 |
//+------------------------------------------------------------------+
void ProcessCSVFile(int fileHandle)
{
   FileSeek(fileHandle, 0, SEEK_SET);
   
   bool isFirstLine = true;
   string newSignals[];
   int signalCount = 0;
   
   // Read all lines
   while(!FileIsEnding(fileHandle))
   {
      string line = FileReadString(fileHandle);
      
      // Skip empty lines
      if(StringLen(line) == 0) continue;
      
      // Skip header line
      if(isFirstLine)
      {
         if(StringFind(line, "timestamp") >= 0)
         {
            isFirstLine = false;
            continue;
         }
         isFirstLine = false;
      }
      
      // Store non-header lines
      ArrayResize(newSignals, signalCount + 1);
      newSignals[signalCount] = line;
      signalCount++;
   }
   
   // Process signals in chronological order
   for(int i = 0; i < signalCount; i++)
   {
      ProcessSingleLine(newSignals[i]);
   }
}

//+------------------------------------------------------------------+
//| Process a single CSV line                                        |
//+------------------------------------------------------------------+
void ProcessSingleLine(string line)
{
   // Parse CSV line manually
   string fields[10];
   int fieldIndex = 0;
   string currentField = "";
   bool inQuotes = false;
   
   for(int i = 0; i < StringLen(line); i++)
   {
      ushort ch = StringGetCharacter(line, i);
      
      if(ch == '"')
      {
         inQuotes = !inQuotes;
      }
      else if(ch == ',' && !inQuotes)
      {
         if(fieldIndex < 10)
         {
            StringTrimLeft(currentField);
            StringTrimRight(currentField);
            fields[fieldIndex] = currentField;
            fieldIndex++;
            currentField = "";
         }
      }
      else
      {
         currentField += ShortToString(ch);
      }
   }
   
   if(fieldIndex < 10)
   {
      StringTrimLeft(currentField);
      StringTrimRight(currentField);
      fields[fieldIndex] = currentField;
      fieldIndex++;
   }
   
   if(fieldIndex < 3) return;
   
   string timestamp = fields[0];
   
   // Skip if already processed
   if(timestamp <= LastProcessedTimestamp && LastProcessedTimestamp != "")
   {
      return;
   }
   
   Print("\n📨 NEW SIGNAL at ", timestamp);
   Print("Raw line: ", line);
   
   string signal_type = fields[1];
   string csvSymbol = fields[2];
   string action = (fieldIndex > 3) ? fields[3] : "";
   string entry_range = (fieldIndex > 4) ? fields[4] : "";
   string sl = (fieldIndex > 5) ? fields[5] : "";
   string tp1 = (fieldIndex > 6) ? fields[6] : "";
   string tp2 = (fieldIndex > 7) ? fields[7] : "";
   string tp3 = (fieldIndex > 8) ? fields[8] : "";
   string tp4 = (fieldIndex > 9) ? fields[9] : "";
   
   Print("Signal Type: ", signal_type);
   Print("Symbol: ", csvSymbol);
   Print("Action: ", action);
   
   if(!IsGoldRelatedSignal(csvSymbol))
   {
      Print("⏭️ Ignoring non-GOLD signal");
      LastProcessedTimestamp = timestamp;
      return;
   }
   
   if(signal_type == "short_signal")
   {
      HandleShortSignal(action);
   }
   else if(signal_type == "full_signal")
   {
      HandleFullSignal(action, entry_range, sl, tp1, tp2, tp3, tp4);
   }
   else if(signal_type == "sltp_update")
   {
      HandleMoveSL(sl);
   }
   else if(signal_type == "breakeven")
   {
      HandleBreakeven();
   }
   else if(signal_type == "close_all")
   {
      HandleCloseAll();
   }
   else if(signal_type == "close_top_entries")
   {
      HandleCloseTopEntries();
   }
   
   LastProcessedTimestamp = timestamp;
}

//+------------------------------------------------------------------+
//| HELPER: Update SL of ALL open positions                          |
//| FIX: Added to support immediate SL update on full_signal         |
//+------------------------------------------------------------------+
void UpdateAllOpenPositions(double newSL)
{
   Print("🔄 Updating ALL positions to SL: ", newSL);
   int total = PositionsTotal();
   for(int i = total - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket > 0 && PositionGetString(POSITION_SYMBOL) == TradingSymbol && PositionGetInteger(POSITION_MAGIC) == MagicNumber)
      {
         MqlTradeRequest request;
         MqlTradeResult result;
         ZeroMemory(request);
         ZeroMemory(result);
         
         request.action = TRADE_ACTION_SLTP;
         request.position = ticket;
         request.symbol = TradingSymbol;
         request.sl = newSL;
         request.tp = PositionGetDouble(POSITION_TP); // Keep existing TP
         
         if(!OrderSend(request, result))
            Print("❌ Failed to update SL for ticket ", ticket, ": ", GetLastError());
         else
            Print("✅ SL Updated for ticket ", ticket);
      }
   }
}

//+------------------------------------------------------------------+
//| SHORT SIGNAL Handler                                             |
//| (Kept intact as per user request, opens initial trade)           |
//+------------------------------------------------------------------+
void HandleShortSignal(string action)
{
   Print("⚡ SHORT SIGNAL: ", action);
   
   double lotSize = CalculateLotSize();
   double currentPrice = (action == "BUY") ? SymbolInfoDouble(TradingSymbol, SYMBOL_ASK) :
                                              SymbolInfoDouble(TradingSymbol, SYMBOL_BID);
   
   ENUM_ORDER_TYPE orderType = (action == "BUY") ? ORDER_TYPE_BUY : ORDER_TYPE_SELL;
   
   MqlTradeRequest request;
   MqlTradeResult result;
   ZeroMemory(request);
   ZeroMemory(result);
   
   request.action = TRADE_ACTION_DEAL;
   request.symbol = TradingSymbol;
   request.volume = lotSize;
   request.type = orderType;
   request.price = currentPrice;
   request.deviation = 10;
   request.magic = MagicNumber;
   request.comment = "Short Signal";
   
   if(OrderSend(request, result))
   {
      Print("✅ SHORT SIGNAL executed: Ticket #", result.order);
   }
   else
   {
      Print("❌ SHORT SIGNAL failed: ", GetLastError());
   }
}

//+------------------------------------------------------------------+
//| FULL SIGNAL Handler - FIXED with Grid Limits                     |
//| FIX 1: Updates SL of short_signal trades immediately             |
//| FIX 2: Uses Limit Orders for better entry pricing                |
//+------------------------------------------------------------------+
void HandleFullSignal(string action, string entry_range, string sl, string tp1, string tp2, string tp3, string tp4)
{
   Print("📊 FULL SIGNAL: ", action, " Range:", entry_range, " SL:", sl);
   
   // 1. UPDATE EXISTING SLs immediately
   double slPrice = StringToDouble(sl);
   UpdateAllOpenPositions(slPrice);
   
   // 2. Parse Range to setup Grid of Limit Orders
   string rangeParts[];
   StringSplit(entry_range, '-', rangeParts);
   if(ArraySize(rangeParts) != 2) return;
   
   double rangeStart = StringToDouble(rangeParts[0]);
   double rangeEnd = StringToDouble(rangeParts[1]);
   
   double upperPrice = MathMax(rangeStart, rangeEnd);
   double lowerPrice = MathMin(rangeStart, rangeEnd);
   
   double currentAsk = SymbolInfoDouble(TradingSymbol, SYMBOL_ASK);
   double currentBid = SymbolInfoDouble(TradingSymbol, SYMBOL_BID);
   double pipGapPoints = PipGapBetweenTrades * PointValue;
   
   // Calculate how many levels fit in the range
   int levels = (int)MathFloor((upperPrice - lowerPrice) / pipGapPoints) + 1;
   Print("Calculated Grid Levels: ", levels);
   if(levels > MaxTradesPerSignal) levels = MaxTradesPerSignal;
   
   double totalLotSize = CalculateLotSize();
   
   // Calculate Lot Per Trade (FIX: Ensure min lot compliance)
   double lotPerTrade = NormalizeDouble(totalLotSize / levels, 2);
   if(lotPerTrade < SymbolInfoDouble(TradingSymbol, SYMBOL_VOLUME_MIN))
   {
      lotPerTrade = SymbolInfoDouble(TradingSymbol, SYMBOL_VOLUME_MIN);
   }
   
   // TP Distribution setup
   double tp1Price = StringToDouble(tp1);
   double tp2Price = StringToDouble(tp2);
   double tp3Price = StringToDouble(tp3);
   
   int tp1Count = (int)MathFloor(levels * TP1_Percentage / 100.0);
   int tp2Count = (int)MathFloor(levels * TP2_Percentage / 100.0);
   int tp3Count = (int)MathFloor(levels * TP3_Percentage / 100.0);
   
   int tpCounter = 0;
   
   for(int i = 0; i < levels; i++)
   {
      double targetEntry = 0;
      if(action == "BUY")
         targetEntry = upperPrice - (i * pipGapPoints); // Start high (upper limit), go down
      else
         targetEntry = lowerPrice + (i * pipGapPoints); // Start low (lower limit), go up
      
      // Assign TP for this level
      double tpPrice = 0;
      if(tpCounter < tp1Count) tpPrice = tp1Price;
      else if(tpCounter < tp1Count + tp2Count) tpPrice = tp2Price;
      else if(tpCounter < tp1Count + tp2Count + tp3Count) tpPrice = tp3Price;
      else tpPrice = 0;
      tpCounter++;
      
      // CHECK: Do we already have a position near this level?
      if(IsPositionNear(targetEntry, pipGapPoints * 0.3)) 
      {
         Print("⏭️ Skipping level ", targetEntry, " - Position exists/covered by short_signal.");
         continue;
      }
      
      MqlTradeRequest request;
      MqlTradeResult result;
      ZeroMemory(request);
      ZeroMemory(result);
      
      request.symbol = TradingSymbol;
      request.volume = lotPerTrade;
      request.sl = slPrice;
      request.tp = tpPrice;
      request.deviation = 10;
      request.magic = MagicNumber;
      request.comment = "Full_Grid";
      
      bool sendOrder = false;
      
      // DECISION: Limit or Market?
      if(action == "BUY")
      {
         if(targetEntry < currentAsk)
         {
            // Better price available -> LIMIT ORDER
            request.action = TRADE_ACTION_PENDING;
            request.type = ORDER_TYPE_BUY_LIMIT;
            request.price = targetEntry;
            sendOrder = true;
         }
         else
         {
             // Price moved away (higher) or is exactly at level.
             // If this is the "best" entry level (i=0) or very close, take it.
             // Otherwise, skip or place limit if retrace expected? 
             // Logic: If price is > targetEntry, a Buy Limit at targetEntry is valid (waiting for drop).
             // Wait, for BUY LIMIT, open_price must be < current_price.
             // If targetEntry > currentAsk (we are below grid), we should BUY STOP into it? 
             // Or just enter Market?
             // Usually signals mean "Limit Orders within range".
             // If current price is BELOW the range, we are getting a great price -> Market Buy?
             // If current price is ABOVE the range, we missed it -> Buy Limit at top of range?
             
             // Let's stick to standard Grid logic:
             // We want to buy at targetEntry.
             if(targetEntry < currentAsk) {
                 request.action = TRADE_ACTION_PENDING;
                 request.type = ORDER_TYPE_BUY_LIMIT;
                 request.price = targetEntry;
                 sendOrder = true;
             } else {
                 // targetEntry >= currentAsk. We are getting a 'better' or 'equal' price now.
                 // Only execute if we are reasonably close to the level (don't buy if price crashed way below)
                 // But wait, if price crashed below, it's an even better buy? 
                 // Let's just Market Buy if we can't Place Limit.
                 request.action = TRADE_ACTION_DEAL;
                 request.type = ORDER_TYPE_BUY;
                 request.price = currentAsk;
                 sendOrder = true;
             }
         }
      }
      else // SELL
      {
         if(targetEntry > currentBid)
         {
            // Better price available -> LIMIT ORDER
            request.action = TRADE_ACTION_PENDING;
            request.type = ORDER_TYPE_SELL_LIMIT;
            request.price = targetEntry;
            sendOrder = true;
         }
         else
         {
            // targetEntry <= currentBid. We are getting a 'better' or 'equal' price now.
            request.action = TRADE_ACTION_DEAL;
            request.type = ORDER_TYPE_SELL;
            request.price = currentBid;
            sendOrder = true;
         }
      }
      
      if(sendOrder)
      {
         if(OrderSend(request, result)) Print("✅ Placed Order/Pending for Level ", targetEntry, ": Ticket ", result.order);
         else Print("❌ Order failed for Level ", targetEntry, ": ", GetLastError());
      }
      
      Sleep(100);
   }
}

//+------------------------------------------------------------------+
//| Helper: Check if a position exists near a price                  |
//+------------------------------------------------------------------+
bool IsPositionNear(double price, double tolerance)
{
   int total = PositionsTotal();
   for(int i = 0; i < total; i++)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket > 0 && PositionGetString(POSITION_SYMBOL) == TradingSymbol && PositionGetInteger(POSITION_MAGIC) == MagicNumber)
      {
         double openPrice = PositionGetDouble(POSITION_PRICE_OPEN);
         if(MathAbs(openPrice - price) <= tolerance) return true;
      }
   }
   return false;
}

void HandleMoveSL(string newSL)
{
   double slPrice = StringToDouble(newSL);
   UpdateAllOpenPositions(slPrice); // Reuse the new helper!
}

void HandleBreakeven()
{
   Print("🔒 BREAKEVEN");
   int total = PositionsTotal();
   int modified = 0;
   
   for(int i = total - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket > 0 && PositionGetString(POSITION_SYMBOL) == TradingSymbol &&
         PositionGetInteger(POSITION_MAGIC) == MagicNumber)
      {
         double openPrice = PositionGetDouble(POSITION_PRICE_OPEN);
         double currentTP = PositionGetDouble(POSITION_TP);
         ENUM_POSITION_TYPE posType = (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
         
         double newSL;
         if(posType == POSITION_TYPE_BUY)
            newSL = openPrice + (BreakevenPips * PointValue);
         else
            newSL = openPrice - (BreakevenPips * PointValue);
         
         MqlTradeRequest request;
         MqlTradeResult result;
         ZeroMemory(request);
         ZeroMemory(result);
         
         request.action = TRADE_ACTION_SLTP;
         request.position = ticket;
         request.symbol = TradingSymbol;
         request.sl = newSL;
         request.tp = currentTP;
         
         if(OrderSend(request, result)) modified++;
      }
   }
   Print("✅ Moved ", modified, " to breakeven");
}

void HandleCloseAll()
{
   Print("🛑 CLOSE ALL");
   int total = PositionsTotal();
   int closed = 0;
   for(int i = total - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket > 0 && PositionGetString(POSITION_SYMBOL) == TradingSymbol &&
         PositionGetInteger(POSITION_MAGIC) == MagicNumber)
      {
         MqlTradeRequest request;
         MqlTradeResult result;
         ZeroMemory(request);
         ZeroMemory(result);
         
         request.action = TRADE_ACTION_DEAL;
         request.position = ticket;
         request.symbol = TradingSymbol;
         request.volume = PositionGetDouble(POSITION_VOLUME);
         request.type = (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY) ? ORDER_TYPE_SELL : ORDER_TYPE_BUY;
         request.price = (request.type == ORDER_TYPE_SELL) ? SymbolInfoDouble(TradingSymbol, SYMBOL_BID) :
                                                               SymbolInfoDouble(TradingSymbol, SYMBOL_ASK);
         request.deviation = 10;
         
         if(OrderSend(request, result)) closed++;
      }
   }
   Print("✅ Closed ", closed, " positions");
}

void HandleCloseTopEntries()
{
   Print("🔻 CLOSE TOP ENTRIES");
   ulong tickets[];
   double openTimes[];
   int count = 0;
   
   int total = PositionsTotal();
   for(int i = 0; i < total; i++)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket > 0 && PositionGetString(POSITION_SYMBOL) == TradingSymbol && PositionGetInteger(POSITION_MAGIC) == MagicNumber)
      {
         ArrayResize(tickets, count + 1);
         ArrayResize(openTimes, count + 1);
         tickets[count] = ticket;
         openTimes[count] = (double)PositionGetInteger(POSITION_TIME);
         count++;
      }
   }
   
   for(int i = 0; i < count - 1; i++)
   {
      for(int j = i + 1; j < count; j++)
      {
         if(openTimes[i] > openTimes[j])
         {
            double tempTime = openTimes[i]; openTimes[i] = openTimes[j]; openTimes[j] = tempTime;
            ulong tempTicket = tickets[i]; tickets[i] = tickets[j]; tickets[j] = tempTicket;
         }
      }
   }
   
   int tradesToClose = (int)MathFloor(count * 0.5);
   int closed = 0;
   for(int i = 0; i < tradesToClose; i++)
   {
      if(PositionSelectByTicket(tickets[i]))
      {
         MqlTradeRequest request;
         MqlTradeResult result;
         ZeroMemory(request);
         ZeroMemory(result);
         request.action = TRADE_ACTION_DEAL;
         request.position = tickets[i];
         request.symbol = TradingSymbol;
         request.volume = PositionGetDouble(POSITION_VOLUME);
         request.type = (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY) ? ORDER_TYPE_SELL : ORDER_TYPE_BUY;
         request.price = (request.type == ORDER_TYPE_SELL) ? SymbolInfoDouble(TradingSymbol, SYMBOL_BID) : SymbolInfoDouble(TradingSymbol, SYMBOL_ASK);
         request.deviation = 10;
         if(OrderSend(request, result)) closed++;
      }
   }
   Print("✅ Closed ", closed, " top entries");
}

double CalculateLotSize()
{
   double lotSize = FixedLotSize;
   if(LotSizeMode == PERCENTAGE_RISK)
   {
      double balance = AccountInfoDouble(ACCOUNT_BALANCE);
      double riskAmount = balance * (RiskPercentage / 100.0);
      double tickValue = SymbolInfoDouble(TradingSymbol, SYMBOL_TRADE_TICK_VALUE);
      double tickSize = SymbolInfoDouble(TradingSymbol, SYMBOL_TRADE_TICK_SIZE);
      double slPips = 100;
      double slInPrice = slPips * PointValue;
      lotSize = (riskAmount / (slInPrice / tickSize * tickValue));
      double minLot = SymbolInfoDouble(TradingSymbol, SYMBOL_VOLUME_MIN);
      double maxLot = SymbolInfoDouble(TradingSymbol, SYMBOL_VOLUME_MAX);
      double lotStep = SymbolInfoDouble(TradingSymbol, SYMBOL_VOLUME_STEP);
      lotSize = MathFloor(lotSize / lotStep) * lotStep;
      lotSize = MathMax(minLot, MathMin(maxLot, lotSize));
   }
   return NormalizeDouble(lotSize, 2);
}

bool IsGoldSymbol(string symbol)
{
   string upperSymbol = symbol;
   StringToUpper(upperSymbol);
   for(int i = 0; i < ArraySize(GoldVariants); i++)
   {
      if(StringFind(upperSymbol, GoldVariants[i]) >= 0) return true;
   }
   return false;
}

string FindGoldSymbolInMarketWatch()
{
   int total = SymbolsTotal(true);
   for(int i = 0; i < total; i++)
   {
      string symbolName = SymbolName(i, true);
      if(IsGoldSymbol(symbolName)) return symbolName;
   }
   return "";
}

bool IsGoldRelatedSignal(string csvSymbol)
{
   string upperSymbol = csvSymbol;
   StringToUpper(upperSymbol);
   for(int i = 0; i < ArraySize(SignalSymbols); i++)
   {
      string upperSignal = SignalSymbols[i];
      StringToUpper(upperSignal);
      if(StringFind(upperSymbol, upperSignal) >= 0 || StringFind(upperSignal, upperSymbol) >= 0) return true;
   }
   if(StringFind(upperSymbol, "GOLD") >= 0 || StringFind(upperSymbol, "XAU") >= 0) return true;
   return false;
}
