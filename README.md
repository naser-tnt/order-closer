# 📦 Order Status Manager

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/naser-tnt/order-closer/main/order_status_app.py)

A lightweight tool to manage and bulk-close orders that haven't been delivered yet — built with Streamlit.

---

## 🚀 Quick Start (Local)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run order_status_app.py
```

The app will open in your browser at `http://localhost:8501`

---

## ☁️ Deploy to Streamlit Community Cloud

1. Push this repo to GitHub (if not already done)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"** → connect your GitHub account
4. Select:
   - **Repository**: `naser-tnt/order-closer`
   - **Branch**: `main`
   - **Main file path**: `order_status_app.py`
5. Click **Deploy!**

---

## 📋 How to Use

1. **Upload CSV**: Click "Browse files" and select your orders CSV file
2. **Review Summary**: See total orders, delivered vs non-delivered counts
3. **View Places**: The app shows a table of all places with non-delivered orders
4. **Exclude Places**: Use the multiselect dropdown to skip places you don't want to process
5. **Close Orders**: Choose your preferred method:
   - **Console Script**: Generates code to paste in browser console (bypasses popup blockers)
   - **Open One by One**: Shows clickable links for each order to open manually
6. **Download**: Export the filtered orders or all non-delivered orders as CSV

---

## 🎯 Features

✅ Automatically filters out "Delivered", "Cancelled", and "Rejected" orders  
✅ Groups non-delivered orders by Place  
✅ Multi-select filtering by location  
✅ One-click console script generation  
✅ Download filtered results as CSV  
✅ Clean, responsive interface  

---

## 📊 CSV Format

Your CSV should include these columns:

| Column | Description |
|--------|-------------|
| `Order ID` | Unique order identifier |
| `Place` | Store/location name |
| `Status` | Order status (e.g., "Order Accepted", "Delivered") |
| `Client` | Customer name |
| `Date` | Order date |
| `Total Price` | Order total |

---

## 🔗 Update URL Format

The app opens URLs in this format:
```
https://bitesnbags.com/updatestatus/delivered/{ORDER_ID}
```

---

## ⚠️ Browser Note

When using the console script, you have full control over opening multiple tabs without triggering popup blockers. Simply:
- Open devtools with `F12` → go to the **Console** tab
- Paste and run the generated script
- Or use the **"Open One by One"** option instead for full control

---

## 💡 Tips

- Start with a few places to test the functionality
- Use the "Open One by One" option for better control
- Download the filtered CSV before closing orders for your records
