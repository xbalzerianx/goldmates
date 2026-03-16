// ============================================================
// KGCAR PRODUCT DATABASE — APPS SCRIPT
// Auto-logs sale to Sales Log when Inventory qty is reduced
// Install: Extensions > Apps Script > paste > Save > Run setup
// ============================================================

function onEdit(e) {
  const sheet = e.source.getActiveSheet();
  const sheetName = sheet.getName();
  
  // Only trigger on INVENTORY tab, column G (Stock Qty = col 7)
  if (sheetName !== "📦 INVENTORY") return;
  
  const col = e.range.getColumn();
  const row = e.range.getRow();
  
  // Column G = 7, only rows 5+ (data rows)
  if (col !== 7 || row < 5) return;
  
  const newQty = e.value ? parseInt(e.value) : 0;
  const oldQty = e.oldValue ? parseInt(e.oldValue) : 0;
  
  // Only trigger if qty DECREASED (a sale happened)
  if (isNaN(newQty) || isNaN(oldQty) || newQty >= oldQty) return;
  
  const qtySold = oldQty - newQty;
  
  // Get product details from the edited row
  const invSheet = e.source.getSheetByName("📦 INVENTORY");
  const productId   = invSheet.getRange(row, 1).getValue();
  const category    = invSheet.getRange(row, 2).getValue();
  const productName = invSheet.getRange(row, 3).getValue();
  const unitPrice   = invSheet.getRange(row, 6).getValue();
  const saleTotal   = qtySold * unitPrice;
  
  // Go to Sales Log tab
  const salesSheet = e.source.getSheetByName("💰 SALES LOG");
  
  // Find next empty row (starting from row 5)
  const lastRow = salesSheet.getLastRow();
  const nextRow = Math.max(lastRow + 1, 5);
  
  // Generate Sale ID (SL-XXXX)
  const saleNum = nextRow - 4; // offset for headers
  const saleId = "SL-" + String(saleNum).padStart(4, "0");
  
  // Today's date
  const today = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "MM/dd/yyyy");
  
  // Write to Sales Log
  salesSheet.getRange(nextRow, 1).setValue(saleId);
  salesSheet.getRange(nextRow, 2).setValue(today);
  salesSheet.getRange(nextRow, 3).setValue(productId);
  salesSheet.getRange(nextRow, 4).setValue(productName);
  salesSheet.getRange(nextRow, 5).setValue(category);
  salesSheet.getRange(nextRow, 6).setValue(qtySold);
  salesSheet.getRange(nextRow, 7).setValue(unitPrice);
  salesSheet.getRange(nextRow, 8).setValue(saleTotal);
  salesSheet.getRange(nextRow, 9).setValue(Session.getActiveUser().getEmail() || "Admin");
  salesSheet.getRange(nextRow, 10).setValue("Auto-logged from Inventory");
  
  // Format the new sales row
  salesSheet.getRange(nextRow, 7, 1, 2).setNumberFormat("#,##0.00");
  
  // Flash notification
  SpreadsheetApp.getActiveSpreadsheet().toast(
    `✅ Sale logged: ${qtySold}x ${productName} = ₱${saleTotal.toLocaleString()}`,
    "KGCAR Sales Logger",
    5
  );
}

// ============================================================
// Run this ONCE manually to set up the installable trigger
// Extensions > Apps Script > select setupTrigger > Run
// ============================================================
function setupTrigger() {
  // Remove existing triggers to avoid duplicates
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(t => {
    if (t.getHandlerFunction() === "onEdit") {
      ScriptApp.deleteTrigger(t);
    }
  });
  
  // Create new installable onEdit trigger
  ScriptApp.newTrigger("onEdit")
    .forSpreadsheet(SpreadsheetApp.getActiveSpreadsheet())
    .onEdit()
    .create();
  
  SpreadsheetApp.getActiveSpreadsheet().toast(
    "✅ KGCAR Auto-Logger is active! Reducing inventory qty will now auto-log sales.",
    "Setup Complete",
    8
  );
}
