import streamlit as st
import pandas as pd
import webbrowser
from io import StringIO

st.set_page_config(
    page_title="Order Status Manager",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Order Status Manager")
st.markdown("Upload your CSV to manage orders that need closing")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(uploaded_file)
    
    # Display basic info
    st.success(f"✅ File uploaded successfully! Total orders: {len(df)}")
    
    # Filter non-processible orders (Delivered, Cancelled, Rejected)
    excluded_statuses = ['Delivered', 'Cancelled', 'Rejected by Place', 'rejected by place', 'Rejected', 'rejected']
    non_delivered_df = df[~df['Status'].isin(excluded_statuses)].copy()
    excluded_df = df[df['Status'].isin(excluded_statuses)].copy()
    
    # Display summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Orders", len(df))
    with col2:
        st.metric("Excluded/Delivered", len(excluded_df))
    with col3:
        st.metric("To Process", len(non_delivered_df))
    
    st.divider()
    
    if len(non_delivered_df) == 0:
        st.info("🎉 All orders are handled (delivered or excluded)! Nothing to process.")
    else:
        # Group by Place and count non-delivered orders
        place_summary = non_delivered_df.groupby('Place').agg({
            'Order ID': 'count',
            'Status': lambda x: ', '.join(x.unique())
        }).reset_index()
        place_summary.columns = ['Place', 'Non-Delivered Count', 'Statuses']
        place_summary = place_summary.sort_values('Non-Delivered Count', ascending=False)
        
        st.subheader("📍 Places Requiring Action")
        st.dataframe(place_summary, use_container_width=True)
        
        st.divider()
        
        # Multi-select for places
        st.subheader("🚫 Exclude Places from Processing")
        
        all_places = place_summary['Place'].tolist()
        default_exclusions = [
            "The Cakery", 
            "Foodz", 
            "OPI Orders", 
            "Secrets Cakes 🇯🇴", 
            "Tip n' Tag Solution"
        ]
        # Only include in default if they actually exist in the current data
        initial_selections = [p for p in default_exclusions if p in all_places]
        
        excluded_places = st.multiselect(
            "Select places you DO NOT want to process (skip):",
            options=all_places,
            default=initial_selections,
            help="Select places to exclude from the batch processing."
        )
        
        # Filter orders - Keep only those NOT in excluded_places
        filtered_orders = non_delivered_df[~non_delivered_df['Place'].isin(excluded_places)].copy()
        
        if len(filtered_orders) > 0:
            st.success(f"📋 Processing {len(filtered_orders)} orders (excluded {len(excluded_places)} places)")
            
            # Display filtered orders
            st.dataframe(
                filtered_orders[['Order ID', 'Place', 'Client', 'Status', 'Total Price', 'Date']],
                use_container_width=True
            )
            
            st.divider()
            
            # Action buttons
            st.subheader("🚀 Close Orders")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Option 1: Console Script")
                st.info("ℹ️ Copy and paste this script into your browser console to open all tabs.")
                
                order_ids = filtered_orders['Order ID'].tolist()
                urls_list = [f"https://bitesnbags.com/updatestatus/delivered/{oid}" for oid in order_ids]
                
                js_script = f"""// Copy this into your browser console (F12)
const urls = {urls_list};
urls.forEach((url, i) => {{
    // 200ms delay between tabs to prevent freezing
    setTimeout(() => window.open(url, '_blank'), i * 200);
}});
console.log('Opening ' + urls.length + ' tabs...');"""
                
                st.code(js_script, language="javascript")
            
            with col2:
                st.markdown("### Option 2: Open One by One")
                st.info("ℹ️ Click links below to open each order individually")
                
                with st.expander("📝 Click to view all links", expanded=True):
                    for idx, row in filtered_orders.iterrows():
                        order_id = row['Order ID']
                        place = row['Place']
                        client = row['Client']
                        url = f"https://bitesnbags.com/updatestatus/delivered/{order_id}"
                        
                        st.markdown(f"**Order {order_id}** - {place} - {client}")
                        st.markdown(f"[🔗 Mark as Delivered]({url})")
                        st.markdown("---")
            
            # Download updated list
            st.divider()
            st.subheader("💾 Download Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Download filtered orders
                csv_filtered = filtered_orders.to_csv(index=False)
                st.download_button(
                    label="📥 Download Selected Orders (CSV)",
                    data=csv_filtered,
                    file_name=f"orders_to_close_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Download all non-delivered
                csv_all_non_delivered = non_delivered_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download All Non-Delivered (CSV)",
                    data=csv_all_non_delivered,
                    file_name=f"all_non_delivered_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        else:
            st.warning("⚠️ All places have been excluded! Please uncheck some places to process orders.")
    
    # Show all data at the bottom
    with st.expander("📊 View All Orders"):
        st.dataframe(df, use_container_width=True)

else:
    st.info("👆 Please upload a CSV file to get started")
    st.markdown("""
    ### Expected CSV Format:
    Your CSV should contain these columns:
    - **Order ID**: Unique order identifier
    - **Place**: Store/location name
    - **Status**: Order status (e.g., "Order Accepted", "Delivered", etc.)
    - Other columns: Client, Client Phone, Date, Total Price, etc.
    """)

# Footer
st.divider()
st.caption("💡 Tip: Use the multiselect to exclude specific places you don't want to process.")
