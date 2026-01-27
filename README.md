# Order Status Manager - Streamlit App

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run order_status_app.py
```

The app will open in your browser at `http://localhost:8501`

## 📋 How to Use

1. **Upload CSV**: Click "Browse files" and select your orders CSV file

2. **Review Summary**: See total orders, delivered vs non-delivered counts

3. **View Places**: The app shows a table of all places with non-delivered orders

4. **Select Places**: Use the multiselect dropdown to choose which places you want to process

5. **Close Orders**: Choose your preferred method:
   - **Open All at Once**: Opens all order update URLs in separate tabs (may be blocked by popup blockers)
   - **Open One by One**: Shows clickable links for each order to open manually

6. **Download**: Export the filtered orders or all non-delivered orders as CSV

## 🎯 Features

✅ Automatically filters out "Delivered" orders  
✅ Groups non-delivered orders by Place  
✅ Multi-select filtering by location  
✅ Two options for opening browser tabs  
✅ Download filtered results  
✅ Clean, responsive interface  

## 📊 CSV Format

Your CSV should include these columns:
- Order ID
- Place
- Status
- Client
- Date
- Total Price
- (other columns are preserved but not required)

## 🔗 Update URL Format

The app opens URLs in this format:
```
https://bitesnbags.com/updatestatus/delivered/{ORDER_ID}
```

## ⚠️ Browser Note

When using "Open All at Once", modern browsers may block multiple popups. You may need to:
- Allow popups for localhost in your browser settings
- Use the "Open One by One" option instead
- Click the browser's "Allow popups" notification

## 💡 Tips

- Start with a few places to test the functionality
- Use the "Open One by One" option for better control
- Download the filtered CSV before closing orders for your records
