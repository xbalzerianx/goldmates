import re

with open('/app/kgcar_index_backup.html', 'r') as f:
    content = f.read()

# ============================================================
# 1. CSS — Work Order styles
# ============================================================
WO_CSS = """
/* ===== WORK ORDER ===== */
.wo-header{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px}
.wo-section{background:#1e2535;border:1px solid #2a3347;border-radius:12px;padding:18px;margin-bottom:14px}
.wo-section-title{font-size:11px;font-weight:700;color:#8a8fa8;text-transform:uppercase;letter-spacing:.07em;margin-bottom:12px}
.wo-items-table{width:100%;border-collapse:collapse;margin-bottom:10px}
.wo-items-table th{font-size:11px;color:#8a8fa8;text-transform:uppercase;letter-spacing:.05em;padding:6px 8px;border-bottom:1px solid #2a3347;text-align:left}
.wo-items-table td{padding:7px 8px;border-bottom:1px solid #1a2030;font-size:13px;color:#e8e0d5;vertical-align:middle}
.wo-totals{background:#151c2c;border-radius:10px;padding:14px 18px;margin-top:10px}
.wo-total-row{display:flex;justify-content:space-between;align-items:center;padding:4px 0;font-size:13px;color:#b0b8cc}
.wo-total-row.grand{font-size:16px;font-weight:700;color:#d4a843;border-top:1px solid #2a3347;margin-top:6px;padding-top:10px}
.wo-status-badge{display:inline-flex;align-items:center;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.05em}
.wo-status-open{background:rgba(212,168,67,.18);color:#d4a843}
.wo-status-inprogress{background:rgba(59,130,246,.18);color:#60a5fa}
.wo-status-completed{background:rgba(34,197,94,.18);color:#4ade80}
.wo-status-cancelled{background:rgba(239,68,68,.18);color:#f87171}
.wo-list-item{background:#1e2535;border:1px solid #2a3347;border-radius:10px;padding:14px 16px;margin-bottom:10px;cursor:pointer;transition:border-color .15s}
.wo-list-item:hover{border-color:#d4a843}
.wo-list-top{display:flex;justify-content:space-between;align-items:flex-start;gap:8px;margin-bottom:6px}
.wo-list-num{font-size:13px;font-weight:700;color:#d4a843}
.wo-list-customer{font-size:14px;font-weight:600;color:#e8e0d5}
.wo-list-sub{font-size:12px;color:#8a8fa8}
.wo-list-total{font-size:14px;font-weight:700;color:#4ade80;white-space:nowrap}
.wo-search-box{display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.wo-search-box input,.wo-search-box select{background:#1e2535;border:1px solid #2a3347;border-radius:8px;padding:9px 13px;font-size:14px;color:#e8e0d5;outline:none;font-size:16px}
.wo-search-box input{flex:1;min-width:180px}
.wo-filter-row{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap}
.wo-filter-btn{padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600;border:1px solid #2a3347;background:#1e2535;color:#8a8fa8;cursor:pointer;transition:all .15s}
.wo-filter-btn.active{background:#d4a843;color:#1a1a1a;border-color:#d4a843}
.wo-add-item-row{display:flex;gap:8px;align-items:flex-end;flex-wrap:wrap;margin-bottom:10px}
.wo-add-item-row .inp,.wo-add-item-row .sel2{flex:1;min-width:120px}
.wo-service-list{display:flex;flex-direction:column;gap:6px;margin-bottom:12px}
.wo-service-item{display:flex;align-items:center;gap:8px;background:#151c2c;border-radius:8px;padding:8px 12px}
.wo-service-item-name{flex:1;font-size:13px;color:#e8e0d5}
.wo-service-item-price{font-size:13px;color:#d4a843;font-weight:600;white-space:nowrap}
.wo-service-item-del{background:none;border:none;color:#f87171;cursor:pointer;font-size:16px;padding:0 4px}
/* templates */
.tpl-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin-bottom:16px}
.tpl-card{background:#1e2535;border:1px solid #2a3347;border-radius:10px;padding:14px;cursor:pointer;transition:border-color .15s}
.tpl-card:hover{border-color:#d4a843}
.tpl-card-name{font-size:14px;font-weight:700;color:#e8e0d5;margin-bottom:4px}
.tpl-card-sub{font-size:12px;color:#8a8fa8}
.tpl-card-actions{display:flex;gap:6px;margin-top:10px}
/* print */
@media print {
  .sidebar,.mob-nav,.topbar,.no-print{display:none!important}
  .main{margin:0!important;padding:0!important}
  .page{display:block!important}
  body{background:#fff;color:#000}
  .wo-print-wrap{max-width:800px;margin:0 auto;padding:20px;font-family:Arial,sans-serif}
  .wo-print-header{display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid #d4a843;padding-bottom:16px;margin-bottom:16px}
  .wo-print-logo{font-size:22px;font-weight:900;color:#000}
  .wo-print-sub{font-size:11px;color:#555}
  .wo-print-info{font-size:12px;color:#333}
  .wo-print-table{width:100%;border-collapse:collapse;margin:12px 0}
  .wo-print-table th{background:#f5f5f5;padding:8px;border:1px solid #ddd;font-size:12px;text-align:left}
  .wo-print-table td{padding:7px 8px;border:1px solid #ddd;font-size:12px}
  .wo-print-totals{margin-left:auto;width:260px;margin-top:10px}
  .wo-print-total-row{display:flex;justify-content:space-between;padding:4px 0;font-size:13px;border-bottom:1px solid #eee}
  .wo-print-total-row.grand{font-size:15px;font-weight:700;border-top:2px solid #000;border-bottom:none;margin-top:4px;padding-top:6px}
  .wo-print-footer{margin-top:30px;display:flex;justify-content:space-between;font-size:11px;color:#555}
  .wo-print-sig{border-top:1px solid #000;width:180px;text-align:center;padding-top:4px;margin-top:40px}
}
@media(max-width:700px){
  .wo-header{grid-template-columns:1fr}
  .wo-add-item-row{flex-direction:column}
  .wo-add-item-row .inp,.wo-add-item-row .sel2{min-width:100%}
  .tpl-list{grid-template-columns:1fr}
}
"""

# Insert before closing </style>
content = content.replace('</style>', WO_CSS + '\n</style>', 1)

# ============================================================
# 2. SIDEBAR — add Work Orders button (after catmgr btn, before sb-footer)
# ============================================================
OLD_SB = 'id="sbCatMgrBtn" style="display:none"><span class="sb-item-icon">🗂️</span>Category Manager\n    </button>'
NEW_SB = OLD_SB + """
    <button class="sb-item" data-page="workorders" onclick="go('workorders')" id="sbWOBtn">
      <span class="sb-item-icon">🔧</span>Work Orders
    </button>
    <button class="sb-item" data-page="wotemplates" onclick="go('wotemplates')" id="sbWOTplBtn" style="display:none">
      <span class="sb-item-icon">📋</span>WO Templates
    </button>"""
content = content.replace(OLD_SB, NEW_SB)

# ============================================================
# 3. MOBILE NAV — add Work Orders button
# ============================================================
OLD_MOB = '<button class="mob-item" data-page="catmgr" onclick="go(\'catmgr\')" id="mobCatMgrBtn" style="display:none"><span class="mob-item-icon">🗂️</span>Categories</button>'
NEW_MOB = OLD_MOB + """
    <button class="mob-item" data-page="workorders" onclick="go('workorders')" id="mobWOBtn"><span class="mob-item-icon">🔧</span>Work Orders</button>"""
content = content.replace(OLD_MOB, NEW_MOB)

# ============================================================
# 4. PAGE HTML — Work Orders + WO Templates pages
# ============================================================
WO_PAGES = """
      <!-- ===== WORK ORDERS PAGE ===== -->
      <div id="page-workorders" class="page">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:20px">
          <div>
            <h1 style="font-size:22px;font-weight:700;color:#e8e0d5;margin:0 0 4px">🔧 Work Orders</h1>
            <p style="font-size:13px;color:#8a8fa8;margin:0">Manage job orders and car service records.</p>
          </div>
          <button class="btn btn-primary no-print" onclick="openNewWO()">+ New Work Order</button>
        </div>
        <!-- filters -->
        <div class="wo-filter-row no-print" id="woFilterRow">
          <button class="wo-filter-btn active" onclick="setWOFilter('all',this)">All</button>
          <button class="wo-filter-btn" onclick="setWOFilter('open',this)">Open</button>
          <button class="wo-filter-btn" onclick="setWOFilter('inprogress',this)">In Progress</button>
          <button class="wo-filter-btn" onclick="setWOFilter('completed',this)">Completed</button>
        </div>
        <div class="wo-search-box no-print">
          <input id="woSearchQ" placeholder="🔍  Search by customer, plate, WO #…" oninput="renderWOList()"/>
        </div>
        <div id="woListWrap">
          <div style="text-align:center;padding:40px;color:#8a8fa8">Loading work orders…</div>
        </div>
      </div>

      <!-- ===== WO TEMPLATES PAGE ===== -->
      <div id="page-wotemplates" class="page">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:20px">
          <div>
            <h1 style="font-size:22px;font-weight:700;color:#e8e0d5;margin:0 0 4px">📋 Work Order Templates</h1>
            <p style="font-size:13px;color:#8a8fa8;margin:0">Create reusable job order templates (e.g. PMS, Brake Job, Change Oil).</p>
          </div>
          <button class="btn btn-primary no-print" onclick="openNewTpl()">+ New Template</button>
        </div>
        <div id="tplListWrap">
          <div style="text-align:center;padding:40px;color:#8a8fa8">Loading templates…</div>
        </div>
      </div>
"""

# Insert before the closing </div></div></div> that wraps .main
OLD_CATMGR_END = '      </div>\n      </div>\n\n    </div>\n  </div>\n</div>\n\n<!-- MOBILE NAV -->'
NEW_CATMGR_END = '      </div>\n      </div>\n' + WO_PAGES + '\n    </div>\n  </div>\n</div>\n\n<!-- MOBILE NAV -->'
content = content.replace(OLD_CATMGR_END, NEW_CATMGR_END)

# ============================================================
# 5. WO DETAIL MODAL
# ============================================================
WO_MODAL = """
<!-- ===== WORK ORDER MODAL ===== -->
<div class="overlay" id="woModal" style="display:none;align-items:flex-start;padding-top:20px">
  <div class="modal" style="max-width:720px;width:98%;max-height:92vh;overflow-y:auto">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <div class="modal-title" id="woModalTitle" style="margin:0">New Work Order</div>
      <button onclick="closeWOModal()" style="background:none;border:none;color:#8a8fa8;font-size:22px;cursor:pointer;line-height:1">&times;</button>
    </div>

    <!-- Header Info -->
    <div class="wo-header">
      <div class="fg"><label class="label">WO Number</label><input class="inp" id="woNum" placeholder="Auto-generated" readonly style="background:#0f1420;color:#d4a843;font-weight:700"/></div>
      <div class="fg"><label class="label">Status</label>
        <select class="sel2" id="woStatus">
          <option value="open">Open</option>
          <option value="inprogress">In Progress</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>
      <div class="fg"><label class="label">Date</label><input class="inp" id="woDate" type="date"/></div>
      <div class="fg"><label class="label">Time</label><input class="inp" id="woTime" type="time"/></div>
    </div>

    <!-- Customer & Vehicle -->
    <div class="wo-section">
      <div class="wo-section-title">Customer & Vehicle</div>
      <div class="wo-header">
        <div class="fg"><label class="label">Customer Name *</label><input class="inp" id="woCustName" placeholder="Juan dela Cruz" style="font-size:16px"/></div>
        <div class="fg"><label class="label">Contact Number</label><input class="inp" id="woCustPhone" placeholder="09XX-XXX-XXXX" style="font-size:16px"/></div>
        <div class="fg"><label class="label">Plate Number</label><input class="inp" id="woPlate" placeholder="ABC 1234" style="font-size:16px;text-transform:uppercase"/></div>
        <div class="fg"><label class="label">Vehicle (Make / Model)</label><input class="inp" id="woVehicle" placeholder="Toyota Vios 2020" style="font-size:16px"/></div>
      </div>
    </div>

    <!-- Mechanic / Worker -->
    <div class="wo-section">
      <div class="wo-section-title">Assigned Mechanic</div>
      <div class="fg"><input class="inp" id="woMechanic" placeholder="e.g. Ramon Cruz" style="font-size:16px"/></div>
    </div>

    <!-- Load Template -->
    <div style="margin-bottom:14px" id="woTplRow">
      <label class="label">Load from Template (optional)</label>
      <select class="sel2" id="woTplSelect" onchange="applyWOTemplate(this.value)" style="width:100%;font-size:16px">
        <option value="">— Pick a template to prefill services & parts —</option>
      </select>
    </div>

    <!-- Services / Labor -->
    <div class="wo-section">
      <div class="wo-section-title">Services / Labor</div>
      <div id="woServiceList" class="wo-service-list"></div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <input class="inp" id="woSvcName" placeholder="Service name (e.g. Change Oil)" style="flex:2;min-width:160px;font-size:16px"
          onkeydown="if(event.key==='Enter'){event.preventDefault();addWOService()}"/>
        <input class="inp" id="woSvcPrice" placeholder="Labor charge ₱" type="number" min="0" style="flex:1;min-width:110px;font-size:16px"
          onkeydown="if(event.key==='Enter'){event.preventDefault();addWOService()}"/>
        <button class="btn btn-primary" onclick="addWOService()" style="white-space:nowrap">+ Add</button>
      </div>
    </div>

    <!-- Parts Used -->
    <div class="wo-section">
      <div class="wo-section-title">Parts Used (from Inventory)</div>
      <div style="position:relative;margin-bottom:12px">
        <input class="inp" id="woPartQ" placeholder="🔍 Search product…" oninput="woPartSearch()" autocomplete="off" style="width:100%;font-size:16px"/>
        <div id="woPartResults" style="display:none;position:absolute;top:100%;left:0;right:0;background:#1e2535;border:1px solid #2a3347;border-radius:0 0 8px 8px;z-index:200;max-height:200px;overflow-y:auto"></div>
      </div>
      <div id="woPartList" class="wo-service-list"></div>
    </div>

    <!-- Notes -->
    <div class="wo-section">
      <div class="wo-section-title">Notes / Remarks</div>
      <textarea class="inp" id="woNotes" rows="2" placeholder="Additional instructions or observations…" style="width:100%;resize:vertical;font-size:16px"></textarea>
    </div>

    <!-- Totals -->
    <div class="wo-totals">
      <div class="wo-total-row"><span>Services / Labor</span><span id="woTtlLabor">₱0.00</span></div>
      <div class="wo-total-row"><span>Parts</span><span id="woTtlParts">₱0.00</span></div>
      <div class="wo-total-row"><span>Subtotal</span><span id="woTtlSub">₱0.00</span></div>
      <div class="wo-total-row"><span>VAT (12%)</span><span id="woTtlVat">₱0.00</span></div>
      <div class="wo-total-row grand"><span>TOTAL</span><span id="woTtlGrand">₱0.00</span></div>
    </div>

    <div style="display:flex;gap:10px;margin-top:18px;flex-wrap:wrap">
      <button class="btn btn-ghost" onclick="closeWOModal()">Cancel</button>
      <button class="btn btn-primary" onclick="saveWO()" id="woSaveBtn">💾 Save Work Order</button>
    </div>
  </div>
</div>

<!-- ===== WO TEMPLATE MODAL ===== -->
<div class="overlay" id="woTplModal" style="display:none;align-items:flex-start;padding-top:20px">
  <div class="modal" style="max-width:620px;width:98%;max-height:90vh;overflow-y:auto">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <div class="modal-title" id="tplModalTitle" style="margin:0">New Template</div>
      <button onclick="closeTplModal()" style="background:none;border:none;color:#8a8fa8;font-size:22px;cursor:pointer;line-height:1">&times;</button>
    </div>
    <div class="fg" style="margin-bottom:12px"><label class="label">Template Name *</label><input class="inp" id="tplName" placeholder="e.g. PMS Package, Change Oil + Filter" style="font-size:16px"/></div>
    <div class="fg" style="margin-bottom:16px"><label class="label">Description</label><input class="inp" id="tplDesc" placeholder="Short description" style="font-size:16px"/></div>

    <!-- Template Services -->
    <div class="wo-section">
      <div class="wo-section-title">Services / Labor</div>
      <div id="tplServiceList" class="wo-service-list"></div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <input class="inp" id="tplSvcName" placeholder="Service name" style="flex:2;min-width:140px;font-size:16px"
          onkeydown="if(event.key==='Enter'){event.preventDefault();addTplService()}"/>
        <input class="inp" id="tplSvcPrice" placeholder="Labor ₱" type="number" min="0" style="flex:1;min-width:100px;font-size:16px"
          onkeydown="if(event.key==='Enter'){event.preventDefault();addTplService()}"/>
        <button class="btn btn-primary" onclick="addTplService()">+ Add</button>
      </div>
    </div>

    <!-- Template Parts -->
    <div class="wo-section">
      <div class="wo-section-title">Preset Parts (optional)</div>
      <div style="position:relative;margin-bottom:12px">
        <input class="inp" id="tplPartQ" placeholder="🔍 Search product…" oninput="tplPartSearch()" autocomplete="off" style="width:100%;font-size:16px"/>
        <div id="tplPartResults" style="display:none;position:absolute;top:100%;left:0;right:0;background:#1e2535;border:1px solid #2a3347;border-radius:0 0 8px 8px;z-index:200;max-height:180px;overflow-y:auto"></div>
      </div>
      <div id="tplPartList" class="wo-service-list"></div>
    </div>

    <div style="display:flex;gap:10px;margin-top:18px;flex-wrap:wrap">
      <button class="btn btn-ghost" onclick="closeTplModal()">Cancel</button>
      <button class="btn btn-primary" onclick="saveTpl()">💾 Save Template</button>
    </div>
  </div>
</div>

<!-- ===== WO PRINT / VIEW MODAL ===== -->
<div class="overlay" id="woPrintModal" style="display:none;align-items:flex-start;padding-top:16px">
  <div class="modal" style="max-width:780px;width:98%;max-height:94vh;overflow-y:auto;background:#fff;color:#111">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px" class="no-print">
      <span style="font-size:15px;font-weight:700;color:#1a1a1a">Work Order Preview</span>
      <div style="display:flex;gap:8px">
        <button onclick="window.print()" style="background:#d4a843;color:#1a1a1a;border:none;border-radius:8px;padding:8px 18px;font-size:13px;font-weight:700;cursor:pointer">🖨️ Print</button>
        <button onclick="closeWOPrint()" style="background:#eee;color:#333;border:none;border-radius:8px;padding:8px 14px;font-size:13px;cursor:pointer">Close</button>
      </div>
    </div>
    <div id="woPrintContent" class="wo-print-wrap"></div>
  </div>
</div>
"""

# Insert WO modals before closing </body>
content = content.replace('</body>', WO_MODAL + '\n</body>', 1)

# ============================================================
# 6. JS — TBL, globals, and all WO functions
# ============================================================
WO_JS = """
// ===================== WORK ORDERS JS =====================
// Add to TBL
TBL.KGWorkOrder = 'kg_work_orders';
TBL.KGWOTemplate = 'kg_wo_templates';

let workOrders = [];
let woTemplates = [];
let currentWOId = null;
let woFilter = 'all';
let woServices = [];   // [{name, price}]
let woParts = [];      // [{id, product_name, qty, unit_price}]
let tplServices = [];
let tplParts = [];
let currentTplId = null;

// ---- WO Number generator ----
function genWONum() {
  const y = new Date().getFullYear();
  const existing = workOrders.filter(w => w.wo_number && w.wo_number.startsWith('WO-' + y));
  const seq = existing.length + 1;
  return 'WO-' + y + '-' + String(seq).padStart(4, '0');
}

// ---- Load WOs ----
async function loadWorkOrders() {
  try {
    [workOrders, woTemplates] = await Promise.all([
      apiGet('KGWorkOrder').catch(() => []),
      apiGet('KGWOTemplate').catch(() => [])
    ]);
    workOrders.sort((a, b) => new Date(b.created_date || 0) - new Date(a.created_date || 0));
  } catch(e) { workOrders = []; woTemplates = []; }
}

// ---- Filter ----
function setWOFilter(f, btn) {
  woFilter = f;
  document.querySelectorAll('#woFilterRow .wo-filter-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderWOList();
}

// ---- Render WO List ----
function renderWOList() {
  const q = (document.getElementById('woSearchQ')?.value || '').toLowerCase().trim();
  let list = workOrders;
  if (woFilter !== 'all') list = list.filter(w => w.status === woFilter);
  if (q) list = list.filter(w => [w.wo_number, w.customer_name, w.plate_number, w.vehicle].join(' ').toLowerCase().includes(q));
  const wrap = document.getElementById('woListWrap');
  if (!wrap) return;
  if (!list.length) {
    wrap.innerHTML = '<div style="text-align:center;padding:40px;color:#8a8fa8">No work orders found.</div>';
    return;
  }
  wrap.innerHTML = list.map(w => {
    const statusClass = {open:'wo-status-open',inprogress:'wo-status-inprogress',completed:'wo-status-completed',cancelled:'wo-status-cancelled'}[w.status] || 'wo-status-open';
    const statusLabel = {open:'Open',inprogress:'In Progress',completed:'Completed',cancelled:'Cancelled'}[w.status] || w.status;
    const svcCount = JSON.parse(w.services_json || '[]').length;
    const partsCount = JSON.parse(w.parts_json || '[]').length;
    return `<div class="wo-list-item" onclick="viewWO('${w.id}')">
      <div class="wo-list-top">
        <div>
          <div class="wo-list-num">${w.wo_number || '—'} &nbsp;<span class="wo-status-badge ${statusClass}">${statusLabel}</span></div>
          <div class="wo-list-customer">${w.customer_name || '—'}</div>
          <div class="wo-list-sub">${w.plate_number ? w.plate_number + ' · ' : ''}${w.vehicle || ''} ${w.mechanic ? '· 🔧 ' + w.mechanic : ''}</div>
          <div class="wo-list-sub">${w.work_date || ''} ${w.work_time || ''} · ${svcCount} service(s) · ${partsCount} part(s)</div>
        </div>
        <div style="text-align:right">
          <div class="wo-list-total">${peso(w.grand_total || 0)}</div>
          <div style="display:flex;gap:6px;margin-top:8px;justify-content:flex-end">
            <button class="btn btn-ghost btn-sm no-print" onclick="event.stopPropagation();openEditWO('${w.id}')">✏️</button>
            <button class="btn btn-ghost btn-sm no-print" onclick="event.stopPropagation();openWOPrint('${w.id}')">🖨️</button>
            <button class="btn btn-ghost btn-sm no-print" onclick="event.stopPropagation();deleteWO('${w.id}')" style="color:#f87171">🗑️</button>
          </div>
        </div>
      </div>
    </div>`;
  }).join('');
}

// ---- Open New WO ----
function openNewWO() {
  currentWOId = null;
  woServices = []; woParts = [];
  document.getElementById('woModalTitle').textContent = '+ New Work Order';
  document.getElementById('woNum').value = genWONum();
  document.getElementById('woStatus').value = 'open';
  const now = new Date();
  document.getElementById('woDate').value = now.toISOString().split('T')[0];
  document.getElementById('woTime').value = now.toTimeString().slice(0,5);
  document.getElementById('woCustName').value = '';
  document.getElementById('woCustPhone').value = '';
  document.getElementById('woPlate').value = '';
  document.getElementById('woVehicle').value = '';
  document.getElementById('woMechanic').value = '';
  document.getElementById('woNotes').value = '';
  document.getElementById('woPartQ').value = '';
  document.getElementById('woPartResults').style.display = 'none';
  populateWOTplSelect();
  renderWOServices(); renderWOParts(); calcWOTotals();
  const m = document.getElementById('woModal');
  m.style.display = 'flex'; m.scrollTop = 0;
}

// ---- Open Edit WO ----
function openEditWO(id) {
  const wo = workOrders.find(w => w.id === id);
  if (!wo) return;
  currentWOId = id;
  woServices = JSON.parse(wo.services_json || '[]');
  woParts = JSON.parse(wo.parts_json || '[]');
  document.getElementById('woModalTitle').textContent = 'Edit ' + (wo.wo_number || 'Work Order');
  document.getElementById('woNum').value = wo.wo_number || '';
  document.getElementById('woStatus').value = wo.status || 'open';
  document.getElementById('woDate').value = wo.work_date || '';
  document.getElementById('woTime').value = wo.work_time || '';
  document.getElementById('woCustName').value = wo.customer_name || '';
  document.getElementById('woCustPhone').value = wo.customer_phone || '';
  document.getElementById('woPlate').value = wo.plate_number || '';
  document.getElementById('woVehicle').value = wo.vehicle || '';
  document.getElementById('woMechanic').value = wo.mechanic || '';
  document.getElementById('woNotes').value = wo.notes || '';
  document.getElementById('woPartQ').value = '';
  document.getElementById('woPartResults').style.display = 'none';
  populateWOTplSelect();
  renderWOServices(); renderWOParts(); calcWOTotals();
  const m = document.getElementById('woModal');
  m.style.display = 'flex'; m.scrollTop = 0;
}

function closeWOModal() {
  document.getElementById('woModal').style.display = 'none';
}

// ---- View WO (just open print preview) ----
function viewWO(id) { openWOPrint(id); }

// ---- Services ----
function addWOService() {
  const name = document.getElementById('woSvcName').value.trim();
  const price = parseFloat(document.getElementById('woSvcPrice').value) || 0;
  if (!name) { toast('Enter a service name.', 'error'); return; }
  woServices.push({ name, price });
  document.getElementById('woSvcName').value = '';
  document.getElementById('woSvcPrice').value = '';
  renderWOServices(); calcWOTotals();
}
function removeWOService(i) { woServices.splice(i, 1); renderWOServices(); calcWOTotals(); }
function renderWOServices() {
  const el = document.getElementById('woServiceList');
  if (!el) return;
  if (!woServices.length) { el.innerHTML = '<div style="color:#8a8fa8;font-size:13px;padding:6px 0">No services added yet.</div>'; return; }
  el.innerHTML = woServices.map((s, i) => `
    <div class="wo-service-item">
      <div class="wo-service-item-name">${s.name}</div>
      <div class="wo-service-item-price">${peso(s.price)}</div>
      <button class="wo-service-item-del" onclick="removeWOService(${i})">×</button>
    </div>`).join('');
}

// ---- Parts search ----
function woPartSearch() {
  const q = document.getElementById('woPartQ').value.toLowerCase().trim();
  const res = document.getElementById('woPartResults');
  if (!q) { res.style.display = 'none'; return; }
  const matches = products.filter(p => [p.product_name, p.brand || '', p.category || ''].join(' ').toLowerCase().includes(q)).slice(0, 8);
  if (!matches.length) { res.style.display = 'none'; return; }
  res.style.display = 'block';
  res.innerHTML = matches.map(p => `
    <div class="prod-item" onclick="pickWOPart('${p.id}')">
      <div><div class="prod-item-name">${p.product_name}</div>
      <div class="prod-item-sub">${p.category || ''} · SRP ${peso(p.unit_price || 0)} · Stock: ${p.stock_qty || 0}</div></div>
    </div>`).join('');
}
function pickWOPart(pid) {
  const p = products.find(x => x.id === pid);
  if (!p) return;
  const existing = woParts.find(x => x.id === pid);
  if (existing) { existing.qty = (existing.qty || 1) + 1; }
  else { woParts.push({ id: p.id, product_name: p.product_name, qty: 1, unit_price: p.unit_price || 0 }); }
  document.getElementById('woPartQ').value = '';
  document.getElementById('woPartResults').style.display = 'none';
  renderWOParts(); calcWOTotals();
}
function removeWOPart(i) { woParts.splice(i, 1); renderWOParts(); calcWOTotals(); }
function renderWOParts() {
  const el = document.getElementById('woPartList');
  if (!el) return;
  if (!woParts.length) { el.innerHTML = '<div style="color:#8a8fa8;font-size:13px;padding:6px 0">No parts added yet.</div>'; return; }
  el.innerHTML = woParts.map((p, i) => `
    <div class="wo-service-item">
      <div class="wo-service-item-name">${p.product_name}
        <span style="margin-left:8px">
          <button onclick="changeWOPartQty(${i},-1)" style="background:#2a3347;border:none;color:#e8e0d5;border-radius:4px;width:22px;height:22px;cursor:pointer;font-size:14px;line-height:1">−</button>
          <span style="margin:0 6px;font-size:13px;color:#d4a843">${p.qty}</span>
          <button onclick="changeWOPartQty(${i},1)" style="background:#2a3347;border:none;color:#e8e0d5;border-radius:4px;width:22px;height:22px;cursor:pointer;font-size:14px;line-height:1">+</button>
        </span>
      </div>
      <div class="wo-service-item-price">${peso((p.unit_price || 0) * (p.qty || 1))}</div>
      <button class="wo-service-item-del" onclick="removeWOPart(${i})">×</button>
    </div>`).join('');
}
function changeWOPartQty(i, delta) {
  woParts[i].qty = Math.max(1, (woParts[i].qty || 1) + delta);
  renderWOParts(); calcWOTotals();
}

// ---- Totals ----
function calcWOTotals() {
  const labor = woServices.reduce((s, x) => s + (x.price || 0), 0);
  const parts = woParts.reduce((s, x) => s + (x.unit_price || 0) * (x.qty || 1), 0);
  const sub = labor + parts;
  const vat = sub * 0.12;
  const grand = sub + vat;
  document.getElementById('woTtlLabor').textContent = peso(labor);
  document.getElementById('woTtlParts').textContent = peso(parts);
  document.getElementById('woTtlSub').textContent = peso(sub);
  document.getElementById('woTtlVat').textContent = peso(vat);
  document.getElementById('woTtlGrand').textContent = peso(grand);
  return { labor, parts, sub, vat, grand };
}

// ---- Template dropdown in WO modal ----
function populateWOTplSelect() {
  const sel = document.getElementById('woTplSelect');
  if (!sel) return;
  sel.innerHTML = '<option value="">— Pick a template to prefill services & parts —</option>' +
    woTemplates.map(t => `<option value="${t.id}">${t.name}</option>`).join('');
}
function applyWOTemplate(id) {
  if (!id) return;
  const tpl = woTemplates.find(t => t.id === id);
  if (!tpl) return;
  woServices = JSON.parse(tpl.services_json || '[]');
  woParts = JSON.parse(tpl.parts_json || '[]');
  renderWOServices(); renderWOParts(); calcWOTotals();
  toast('Template "' + tpl.name + '" applied!', 'success');
}

// ---- Save WO ----
async function saveWO() {
  const custName = document.getElementById('woCustName').value.trim();
  if (!custName) { toast('Customer name is required.', 'error'); return; }
  const t = calcWOTotals();
  const payload = {
    wo_number: document.getElementById('woNum').value,
    status: document.getElementById('woStatus').value,
    work_date: document.getElementById('woDate').value,
    work_time: document.getElementById('woTime').value,
    customer_name: custName,
    customer_phone: document.getElementById('woCustPhone').value.trim(),
    plate_number: document.getElementById('woPlate').value.trim().toUpperCase(),
    vehicle: document.getElementById('woVehicle').value.trim(),
    mechanic: document.getElementById('woMechanic').value.trim(),
    notes: document.getElementById('woNotes').value.trim(),
    services_json: JSON.stringify(woServices),
    parts_json: JSON.stringify(woParts),
    labor_total: t.labor,
    parts_total: t.parts,
    subtotal: t.sub,
    vat_amount: t.vat,
    grand_total: t.grand,
    recorded_by: currentUser?.name || 'Admin'
  };
  const btn = document.getElementById('woSaveBtn');
  btn.disabled = true; btn.textContent = 'Saving…';
  try {
    if (currentWOId) {
      await apiPut('KGWorkOrder', currentWOId, payload);
      const idx = workOrders.findIndex(w => w.id === currentWOId);
      if (idx > -1) workOrders[idx] = { ...workOrders[idx], ...payload };
      toast('Work order updated!', 'success');
    } else {
      const saved = await apiPost('KGWorkOrder', payload);
      workOrders.unshift(saved);
      toast('Work order saved!', 'success');
    }
    closeWOModal();
    renderWOList();
  } catch(e) {
    toast('Error saving: ' + e.message, 'error');
  } finally {
    btn.disabled = false; btn.textContent = '💾 Save Work Order';
  }
}

// ---- Delete WO ----
function deleteWO(id) {
  if (!confirm('Delete this work order?')) return;
  apiDel('KGWorkOrder', id).then(() => {
    workOrders = workOrders.filter(w => w.id !== id);
    renderWOList();
    toast('Deleted.', 'success');
  }).catch(e => toast('Error: ' + e.message, 'error'));
}

// ---- Print WO ----
function openWOPrint(id) {
  const wo = workOrders.find(w => w.id === id);
  if (!wo) return;
  const services = JSON.parse(wo.services_json || '[]');
  const parts = JSON.parse(wo.parts_json || '[]');
  const labor = wo.labor_total || 0;
  const partsTotal = wo.parts_total || 0;
  const sub = wo.subtotal || 0;
  const vat = wo.vat_amount || 0;
  const grand = wo.grand_total || 0;
  const statusLabel = {open:'Open',inprogress:'In Progress',completed:'Completed',cancelled:'Cancelled'}[wo.status] || wo.status;

  const html = `
  <div class="wo-print-wrap">
    <div class="wo-print-header">
      <div>
        <div class="wo-print-logo">🔧 KGCAR</div>
        <div class="wo-print-sub">Car Service Work Order</div>
      </div>
      <div class="wo-print-info" style="text-align:right">
        <div><strong>${wo.wo_number || '—'}</strong></div>
        <div>Date: ${wo.work_date || '—'} ${wo.work_time || ''}</div>
        <div>Status: <strong>${statusLabel}</strong></div>
      </div>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:16px;font-size:12px">
      <div>
        <div style="font-weight:700;margin-bottom:4px;color:#555">CUSTOMER</div>
        <div><strong>${wo.customer_name || '—'}</strong></div>
        <div>${wo.customer_phone || ''}</div>
      </div>
      <div>
        <div style="font-weight:700;margin-bottom:4px;color:#555">VEHICLE</div>
        <div>${wo.plate_number || '—'}</div>
        <div>${wo.vehicle || ''}</div>
      </div>
      <div>
        <div style="font-weight:700;margin-bottom:4px;color:#555">MECHANIC</div>
        <div>${wo.mechanic || '—'}</div>
      </div>
      <div>
        <div style="font-weight:700;margin-bottom:4px;color:#555">RECORDED BY</div>
        <div>${wo.recorded_by || '—'}</div>
      </div>
    </div>

    ${services.length ? `
    <div style="font-weight:700;font-size:13px;margin-bottom:6px">Services / Labor</div>
    <table class="wo-print-table">
      <thead><tr><th>Service Description</th><th style="text-align:right">Charge</th></tr></thead>
      <tbody>${services.map(s => `<tr><td>${s.name}</td><td style="text-align:right">${peso(s.price)}</td></tr>`).join('')}</tbody>
    </table>` : ''}

    ${parts.length ? `
    <div style="font-weight:700;font-size:13px;margin:12px 0 6px">Parts Used</div>
    <table class="wo-print-table">
      <thead><tr><th>Part / Product</th><th style="text-align:right">Qty</th><th style="text-align:right">Unit Price</th><th style="text-align:right">Amount</th></tr></thead>
      <tbody>${parts.map(p => `<tr><td>${p.product_name}</td><td style="text-align:right">${p.qty}</td><td style="text-align:right">${peso(p.unit_price)}</td><td style="text-align:right">${peso(p.unit_price * p.qty)}</td></tr>`).join('')}</tbody>
    </table>` : ''}

    ${wo.notes ? `<div style="margin:12px 0;font-size:12px"><strong>Notes:</strong> ${wo.notes}</div>` : ''}

    <div class="wo-print-totals">
      <div class="wo-print-total-row"><span>Services / Labor</span><span>${peso(labor)}</span></div>
      <div class="wo-print-total-row"><span>Parts</span><span>${peso(partsTotal)}</span></div>
      <div class="wo-print-total-row"><span>Subtotal</span><span>${peso(sub)}</span></div>
      <div class="wo-print-total-row"><span>VAT (12%)</span><span>${peso(vat)}</span></div>
      <div class="wo-print-total-row grand"><span>GRAND TOTAL</span><span>${peso(grand)}</span></div>
    </div>

    <div class="wo-print-footer">
      <div>
        <div class="wo-print-sig">Customer Signature</div>
      </div>
      <div>
        <div class="wo-print-sig">Authorized by</div>
      </div>
      <div style="font-size:10px;color:#888;align-self:flex-end">
        Printed: ${new Date().toLocaleString('en-PH')}<br>
        Thank you for trusting KGCAR!
      </div>
    </div>
  </div>`;

  document.getElementById('woPrintContent').innerHTML = html;
  document.getElementById('woPrintModal').style.display = 'flex';
}
function closeWOPrint() {
  document.getElementById('woPrintModal').style.display = 'none';
}

// ---- TEMPLATES ----
function openNewTpl() {
  currentTplId = null; tplServices = []; tplParts = [];
  document.getElementById('tplModalTitle').textContent = '+ New Template';
  document.getElementById('tplName').value = '';
  document.getElementById('tplDesc').value = '';
  document.getElementById('tplSvcName').value = '';
  document.getElementById('tplSvcPrice').value = '';
  document.getElementById('tplPartQ').value = '';
  document.getElementById('tplPartResults').style.display = 'none';
  renderTplServices(); renderTplParts();
  document.getElementById('woTplModal').style.display = 'flex';
}
function openEditTpl(id) {
  const tpl = woTemplates.find(t => t.id === id);
  if (!tpl) return;
  currentTplId = id;
  tplServices = JSON.parse(tpl.services_json || '[]');
  tplParts = JSON.parse(tpl.parts_json || '[]');
  document.getElementById('tplModalTitle').textContent = 'Edit: ' + tpl.name;
  document.getElementById('tplName').value = tpl.name || '';
  document.getElementById('tplDesc').value = tpl.description || '';
  document.getElementById('tplPartQ').value = '';
  document.getElementById('tplPartResults').style.display = 'none';
  renderTplServices(); renderTplParts();
  document.getElementById('woTplModal').style.display = 'flex';
}
function closeTplModal() { document.getElementById('woTplModal').style.display = 'none'; }

function addTplService() {
  const name = document.getElementById('tplSvcName').value.trim();
  const price = parseFloat(document.getElementById('tplSvcPrice').value) || 0;
  if (!name) return;
  tplServices.push({ name, price });
  document.getElementById('tplSvcName').value = '';
  document.getElementById('tplSvcPrice').value = '';
  renderTplServices();
}
function removeTplService(i) { tplServices.splice(i, 1); renderTplServices(); }
function renderTplServices() {
  const el = document.getElementById('tplServiceList');
  if (!el) return;
  el.innerHTML = tplServices.length
    ? tplServices.map((s, i) => `<div class="wo-service-item"><div class="wo-service-item-name">${s.name}</div><div class="wo-service-item-price">${peso(s.price)}</div><button class="wo-service-item-del" onclick="removeTplService(${i})">×</button></div>`).join('')
    : '<div style="color:#8a8fa8;font-size:13px;padding:6px 0">No services yet.</div>';
}

function tplPartSearch() {
  const q = document.getElementById('tplPartQ').value.toLowerCase().trim();
  const res = document.getElementById('tplPartResults');
  if (!q) { res.style.display = 'none'; return; }
  const matches = products.filter(p => [p.product_name, p.brand || ''].join(' ').toLowerCase().includes(q)).slice(0, 8);
  if (!matches.length) { res.style.display = 'none'; return; }
  res.style.display = 'block';
  res.innerHTML = matches.map(p => `<div class="prod-item" onclick="pickTplPart('${p.id}')"><div class="prod-item-name">${p.product_name}</div><div class="prod-item-sub">${p.category || ''} · ${peso(p.unit_price || 0)}</div></div>`).join('');
}
function pickTplPart(pid) {
  const p = products.find(x => x.id === pid);
  if (!p) return;
  if (!tplParts.find(x => x.id === pid)) tplParts.push({ id: p.id, product_name: p.product_name, qty: 1, unit_price: p.unit_price || 0 });
  document.getElementById('tplPartQ').value = '';
  document.getElementById('tplPartResults').style.display = 'none';
  renderTplParts();
}
function removeTplPart(i) { tplParts.splice(i, 1); renderTplParts(); }
function renderTplParts() {
  const el = document.getElementById('tplPartList');
  if (!el) return;
  el.innerHTML = tplParts.length
    ? tplParts.map((p, i) => `<div class="wo-service-item"><div class="wo-service-item-name">${p.product_name}</div><div class="wo-service-item-price">${peso(p.unit_price)}</div><button class="wo-service-item-del" onclick="removeTplPart(${i})">×</button></div>`).join('')
    : '<div style="color:#8a8fa8;font-size:13px;padding:6px 0">No parts added.</div>';
}

async function saveTpl() {
  const name = document.getElementById('tplName').value.trim();
  if (!name) { toast('Template name is required.', 'error'); return; }
  const payload = {
    name,
    description: document.getElementById('tplDesc').value.trim(),
    services_json: JSON.stringify(tplServices),
    parts_json: JSON.stringify(tplParts)
  };
  try {
    if (currentTplId) {
      await apiPut('KGWOTemplate', currentTplId, payload);
      const idx = woTemplates.findIndex(t => t.id === currentTplId);
      if (idx > -1) woTemplates[idx] = { ...woTemplates[idx], ...payload };
      toast('Template updated!', 'success');
    } else {
      const saved = await apiPost('KGWOTemplate', payload);
      woTemplates.unshift(saved);
      toast('Template saved!', 'success');
    }
    closeTplModal();
    renderTplList();
  } catch(e) { toast('Error: ' + e.message, 'error'); }
}

function deleteTpl(id) {
  if (!confirm('Delete this template?')) return;
  apiDel('KGWOTemplate', id).then(() => {
    woTemplates = woTemplates.filter(t => t.id !== id);
    renderTplList();
    toast('Deleted.', 'success');
  }).catch(e => toast('Error: ' + e.message, 'error'));
}

function renderTplList() {
  const wrap = document.getElementById('tplListWrap');
  if (!wrap) return;
  if (!woTemplates.length) {
    wrap.innerHTML = '<div style="text-align:center;padding:40px;color:#8a8fa8">No templates yet. Create one to speed up your work orders!</div>';
    return;
  }
  wrap.innerHTML = '<div class="tpl-list">' + woTemplates.map(t => {
    const svcs = JSON.parse(t.services_json || '[]');
    const parts = JSON.parse(t.parts_json || '[]');
    return `<div class="tpl-card" onclick="openEditTpl('${t.id}')">
      <div class="tpl-card-name">📋 ${t.name}</div>
      <div class="tpl-card-sub">${t.description || ''}</div>
      <div class="tpl-card-sub" style="margin-top:6px">${svcs.length} service(s) · ${parts.length} preset part(s)</div>
      <div class="tpl-card-actions">
        <button class="btn btn-ghost btn-sm" onclick="event.stopPropagation();openEditTpl('${t.id}')">✏️ Edit</button>
        <button class="btn btn-ghost btn-sm" onclick="event.stopPropagation();deleteTpl('${t.id}')" style="color:#f87171">🗑️</button>
      </div>
    </div>`;
  }).join('') + '</div>';
}

// ===================== END WORK ORDERS JS =====================
"""

# Find the right spot — insert right before the final </script>
# Add it right before the last </script> tag
last_script = content.rfind('</script>')
content = content[:last_script] + WO_JS + '\n</script>' + content[last_script+9:]

# ============================================================
# 7. TITLES map — add workorders & wotemplates
# ============================================================
content = content.replace(
    "const TITLES={dashboard:'Dashboard',inventory:'Products & Inventory',sale:'Record Sale',saleslog:'Sales Log',expenses:'Expenses',actlog:'Activity Log',alerts:'Stock Alerts',catmgr:'Category Manager'};",
    "const TITLES={dashboard:'Dashboard',inventory:'Products & Inventory',sale:'Record Sale',saleslog:'Sales Log',expenses:'Expenses',actlog:'Activity Log',alerts:'Stock Alerts',catmgr:'Category Manager',workorders:'Work Orders',wotemplates:'WO Templates'};"
)

# ============================================================
# 8. go() — handle workorders / wotemplates page nav
# ============================================================
OLD_GO_CATMGR = "  if(page==='catmgr'){"
NEW_GO = """  if(page==='workorders'){loadWorkOrders().then(()=>renderWOList());}
  if(page==='wotemplates'){loadWorkOrders().then(()=>renderTplList());}
  if(page==='catmgr'){"""
content = content.replace(OLD_GO_CATMGR, NEW_GO, 1)

# ============================================================
# 9. launchApp — show WO Templates btn for Admin only
# ============================================================
OLD_LAUNCH = "  const cpBtn=document.getElementById('sbChangePinBtn');"
NEW_LAUNCH = """  const woTplBtn=document.getElementById('sbWOTplBtn');
  if(woTplBtn) woTplBtn.style.display = (currentUser?.role==='admin') ? '' : 'none';
  const cpBtn=document.getElementById('sbChangePinBtn');"""
content = content.replace(OLD_LAUNCH, NEW_LAUNCH, 1)

with open('/app/kgcar_index_v31.html', 'w') as f:
    f.write(content)

print(f"Done. Output size: {len(content)} chars / {content.count(chr(10))} lines")

# Quick sanity checks
assert 'page-workorders' in content, "MISSING: page-workorders"
assert 'page-wotemplates' in content, "MISSING: page-wotemplates"
assert 'woModal' in content, "MISSING: woModal"
assert 'woPrintModal' in content, "MISSING: woPrintModal"
assert 'woTplModal' in content, "MISSING: woTplModal"
assert 'KGWorkOrder' in content, "MISSING: KGWorkOrder"
assert 'KGWOTemplate' in content, "MISSING: KGWOTemplate"
assert 'calcWOTotals' in content, "MISSING: calcWOTotals"
assert 'openWOPrint' in content, "MISSING: openWOPrint"
print("All sanity checks passed ✅")
