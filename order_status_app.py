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
st.markdown("Upload your CSV to manage non-delivered orders")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(uploaded_file)
    
    # Display basic info
    st.success(f"✅ File uploaded successfully! Total orders: {len(df)}")
    
    # Filter non-delivered orders
    non_delivered_df = df[df['Status'] != 'Delivered'].copy()
    delivered_df = df[df['Status'] == 'Delivered'].copy()
    
    # Display summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Orders", len(df))
    with col2:
        st.metric("Delivered", len(delivered_df))
    with col3:
        st.metric("Non-Delivered", len(non_delivered_df))
    
    st.divider()
    
    if len(non_delivered_df) == 0:
        st.info("🎉 All orders are delivered! Nothing to process.")
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
        st.subheader("🎯 Select Places to Process")
        selected_places = st.multiselect(
            "Choose which places you want to close orders for:",
            options=place_summary['Place'].tolist(),
            default=None,
            help="Select one or more places to view and close their non-delivered orders"
        )
        
        if selected_places:
            # Filter orders for selected places
            filtered_orders = non_delivered_df[non_delivered_df['Place'].isin(selected_places)].copy()
            
            st.success(f"📋 Found {len(filtered_orders)} non-delivered orders for selected places")
            
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
                st.markdown("### Option 1: Open All at Once")
                st.warning("⚠️ This will open multiple browser tabs at once. May be blocked by popup blockers.")
                
                if st.button("🔗 Open All Tabs", type="primary", use_container_width=True):
                    order_ids = filtered_orders['Order ID'].tolist()
                    
                    # Generate HTML with JavaScript to open all tabs
                    html_code = """
                    <script>
                    function openAllTabs() {
                        var orderIds = """ + str(order_ids) + """;
                        orderIds.forEach(function(orderId) {
                            window.open('https://bitesnbags.com/updatestatus/delivered/' + orderId, '_blank');
                        });
                        alert('Attempted to open ' + orderIds.length + ' tabs. Check if your browser blocked any popups.');
                    }
                    openAllTabs();
                    </script>
                    """
                    st.components.v1.html(html_code, height=0)
                    st.success(f"✅ Attempted to open {len(order_ids)} tabs!")
            
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
            st.info("👆 Please select at least one place to view and process orders")
    
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
st.caption("💡 Tip: Use the multiselect to filter specific places, then choose how you want to open the order update links.")
