import streamlit as st
import pandas as pd
import os
from datetime import datetime
import json
import base64
from PIL import Image
import io

# 设置页面配置
st.set_page_config(
    page_title="资产管理平台",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 数据文件路径
DATA_DIR = "data"
PRINT_MATERIALS_FILE = os.path.join(DATA_DIR, "print_materials.xlsx")
ACCESSORIES_FILE = os.path.join(DATA_DIR, "accessories.xlsx")
PACKAGING_FILE = os.path.join(DATA_DIR, "packaging.xlsx")

# 图片目录路径
IMAGES_DIR = os.path.join(DATA_DIR, "images")
MATERIALS_IMAGES_DIR = os.path.join(IMAGES_DIR, "materials")
ACCESSORIES_IMAGES_DIR = os.path.join(IMAGES_DIR, "accessories")
PACKAGING_IMAGES_DIR = os.path.join(IMAGES_DIR, "packaging")

# 确保数据目录和图片目录存在
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(MATERIALS_IMAGES_DIR, exist_ok=True)
os.makedirs(ACCESSORIES_IMAGES_DIR, exist_ok=True)
os.makedirs(PACKAGING_IMAGES_DIR, exist_ok=True)

def load_data(file_path):
    """加载Excel数据"""
    if os.path.exists(file_path):
        try:
            return pd.read_excel(file_path)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def save_data(df, file_path):
    """保存数据到Excel"""
    df.to_excel(file_path, index=False)

def calculate_cost_per_gram(row):
    """计算每克成本"""
    return (row['购买价'] + row['运费']) / row['总克重']

def calculate_cost_per_unit(row):
    """计算每单位成本"""
    return (row['购买价'] + row['运费']) / row['总数量']

def save_uploaded_image(uploaded_file, image_dir, filename):
    """保存上传的图片"""
    if uploaded_file is not None:
        # 确保文件名唯一
        file_extension = os.path.splitext(uploaded_file.name)[1]
        if not filename.endswith(file_extension):
            filename += file_extension
        
        file_path = os.path.join(image_dir, filename)
        
        # 保存图片
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path
    return None

def display_image(image_path, width=200):
    """显示图片"""
    if image_path and os.path.exists(image_path):
        try:
            image = Image.open(image_path)
            st.image(image, width=width, caption="产品图片")
        except Exception as e:
            st.error(f"图片加载失败: {e}")
    else:
        st.info("暂无图片")

def get_image_path(image_dir, filename):
    """获取图片路径，兼容空、NaN、float等异常情况"""
    if not filename or not isinstance(filename, str) or filename.lower() == 'nan':
        return None
    # 尝试不同的文件扩展名
    for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        file_path = os.path.join(image_dir, filename + ext)
        if os.path.exists(file_path):
            return file_path
    # 也尝试无扩展名
    file_path = os.path.join(image_dir, filename)
    if os.path.exists(file_path):
        return file_path
    return None

def save_history_record(record, file_path):
    """保存历史记录到Excel"""
    import pandas as pd
    import os
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])
    df.to_excel(file_path, index=False)

def load_history_records(file_path):
    import pandas as pd
    import os
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    return pd.DataFrame()

def clear_history_records(file_path):
    import os
    if os.path.exists(file_path):
        os.remove(file_path)

def card_multiselect(options, images_dir, df, label, session_key):
    import streamlit as st
    # 初始化session_state
    if session_key not in st.session_state:
        st.session_state[session_key] = set()
    selected = st.session_state[session_key]
    st.write(f"**{label}**（点击图片或标题选择/取消）")
    cols = st.columns(6)
    for i, option in enumerate(options):
        with cols[i % 6]:
            row = df[df['名称'] == option].iloc[0]
            image_path = get_image_path(images_dir, row.get('图片路径', ''))
            is_selected = option in selected
            btn_label = f"{'✅ ' if is_selected else ''}{option}"
            # 显示图片
            if image_path:
                st.image(image_path, width=100)
            # 显示标题按钮
            if st.button(btn_label, key=f"{session_key}_{option}"):
                if is_selected:
                    selected.remove(option)
                else:
                    selected.add(option)
                st.session_state[session_key] = selected.copy()
                st.rerun()
    return list(selected)

def main():
    st.title("📊 资产管理平台")
    
    # 侧边栏导航
    page = st.sidebar.radio(
        "选择页面",
        ["主页面 - 产品价格计算", "打印材料管理", "产品配件管理", "包装管理"]
    )
    
    if page == "主页面 - 产品价格计算":
        show_main_page()
    elif page == "打印材料管理":
        show_print_materials_page()
    elif page == "产品配件管理":
        show_accessories_page()
    elif page == "包装管理":
        show_packaging_page()

def show_main_page():
    st.header("🏠 主页面 - 产品价格计算")
    
    # 加载数据
    print_materials_df = load_data(PRINT_MATERIALS_FILE)
    accessories_df = load_data(ACCESSORIES_FILE)
    packaging_df = load_data(PACKAGING_FILE)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("输入参数")
        
        # 克重输入
        weight = st.number_input("克重 (克)", min_value=0.0, value=0.0, step=0.1)
        
        # 打印材料选择
        if not print_materials_df.empty:
            print_material_options = print_materials_df['名称'].tolist()
            selected_print_material = st.selectbox("打印材料", print_material_options)
            
            # 显示选中的打印材料图片
            if selected_print_material:
                material_row = print_materials_df[print_materials_df['名称'] == selected_print_material].iloc[0]
                if '图片路径' in material_row and material_row['图片路径']:
                    image_path = get_image_path(MATERIALS_IMAGES_DIR, material_row['图片路径'])
                    display_image(image_path, width=150)
        else:
            st.warning("请先在打印材料管理页面添加材料")
            selected_print_material = None
        
        # 产品配件卡片多选
        if not accessories_df.empty:
            accessory_options = accessories_df['名称'].tolist()
            selected_accessories = card_multiselect(accessory_options, ACCESSORIES_IMAGES_DIR, accessories_df, "产品配件 (可多选)", "selected_accessories")
        else:
            st.warning("请先在产品配件管理页面添加配件")
            selected_accessories = []
        
        # 包装卡片多选
        if not packaging_df.empty:
            packaging_options = packaging_df['名称'].tolist()
            selected_packaging = card_multiselect(packaging_options, PACKAGING_IMAGES_DIR, packaging_df, "包装 (可多选)", "selected_packaging")
        else:
            st.warning("请先在包装管理页面添加包装")
            selected_packaging = []
    
    with col2:
        st.subheader("计算结果")
        
        if st.button("计算价格", type="primary"):
            if selected_print_material is None:
                st.error("请选择打印材料")
                return
            
            # 计算打印材料成本
            material_row = print_materials_df[print_materials_df['名称'] == selected_print_material].iloc[0]
            material_cost = weight * material_row['每克成本']
            
            # 计算配件成本
            accessories_cost = 0
            if selected_accessories:
                for accessory in selected_accessories:
                    accessory_row = accessories_df[accessories_df['名称'] == accessory].iloc[0]
                    accessories_cost += accessory_row['每单位成本']
            
            # 计算包装成本
            packaging_cost = 0
            if selected_packaging:
                for package in selected_packaging:
                    package_row = packaging_df[packaging_df['名称'] == package].iloc[0]
                    packaging_cost += package_row['每单位成本']
            
            # 总成本
            total_cost = material_cost + accessories_cost + packaging_cost
            
            # 显示结果
            st.metric("打印材料成本", f"¥{material_cost:.2f}")
            st.metric("产品配件成本", f"¥{accessories_cost:.2f}")
            st.metric("包装成本", f"¥{packaging_cost:.2f}")
            st.metric("总成本", f"¥{total_cost:.2f}", delta=f"¥{total_cost:.2f}")
            
            # 详细计算过程
            with st.expander("查看详细计算过程"):
                st.write(f"**计算公式**: 克重 × 打印材料每克成本 + 产品配件 + 包装")
                st.write(f"**克重**: {weight} 克")
                st.write(f"**打印材料**: {selected_print_material} (每克成本: ¥{material_row['每克成本']:.4f})")
                st.write(f"**打印材料成本**: {weight} × ¥{material_row['每克成本']:.4f} = ¥{material_cost:.2f}")
                
                if selected_accessories:
                    st.write("**产品配件**:")
                    for accessory in selected_accessories:
                        accessory_row = accessories_df[accessories_df['名称'] == accessory].iloc[0]
                        st.write(f"  - {accessory}: ¥{accessory_row['每单位成本']:.2f}")
                
                if selected_packaging:
                    st.write("**包装**:")
                    for package in selected_packaging:
                        package_row = packaging_df[packaging_df['名称'] == package].iloc[0]
                        st.write(f"  - {package}: ¥{package_row['每单位成本']:.2f}")
            
            # 保存历史记录
            from datetime import datetime
            record = {
                '时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                '克重': weight,
                '打印材料': selected_print_material,
                '打印材料成本': material_cost,
                '产品配件': ','.join(selected_accessories) if selected_accessories else '',
                '配件成本': accessories_cost,
                '包装': ','.join(selected_packaging) if selected_packaging else '',
                '包装成本': packaging_cost,
                '总成本': total_cost
            }
            save_history_record(record, os.path.join(DATA_DIR, 'history_costs.xlsx'))
    
    # 历史计算成本
    st.subheader("历史计算成本")
    history_file = os.path.join(DATA_DIR, 'history_costs.xlsx')
    history_df = load_history_records(history_file)
    if not history_df.empty:
        st.dataframe(history_df, use_container_width=True)
        if st.button("清空历史记录", type="secondary"):
            clear_history_records(history_file)
            st.success("历史记录已清空")
            st.rerun()
    else:
        st.info("暂无历史计算记录")

def show_print_materials_page():
    st.header("🖨️ 打印材料管理")
    
    # 加载数据
    df = load_data(PRINT_MATERIALS_FILE)
    
    # 如果没有数据，创建空的DataFrame
    if df.empty:
        df = pd.DataFrame(columns=['名称', '品牌', '质感', '耗材颜色', '耗材类型', '购买价', '运费', '总克重', '购买时间', '每克成本', '图片路径', '链接', '备注'])
    # 补全旧数据缺失的列
    for col in ['品牌', '质感', '耗材颜色', '耗材类型', '链接', '备注']:
        if col not in df.columns:
            df[col] = ''
    
    # 添加新材料的表单
    with st.expander("添加新材料", expanded=True):
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
        
        with col1:
            name = st.text_input("名称")
        with col2:
            brand = st.text_input("品牌")
        with col3:
            texture = st.text_input("质感")
        with col4:
            color = st.text_input("耗材颜色")
        with col5:
            material_type = st.text_input("耗材类型")
        with col6:
            purchase_price = st.number_input("购买价 (元)", min_value=0.0, value=0.0, step=0.01)
        with col7:
            shipping_fee = st.number_input("运费 (元)", min_value=0.0, value=0.0, step=0.01)
        with col8:
            total_weight = st.number_input("总克重 (克)", min_value=0.0, value=0.0, step=0.1)
        purchase_date = st.date_input("购买时间", value=datetime.now())
        link = st.text_input("链接", placeholder="购买链接或产品链接")
        remark = st.text_area("备注", placeholder="额外说明信息")
        uploaded_image = st.file_uploader("上传图片", type=['jpg', 'jpeg', 'png', 'gif'], key="material_upload")
        if st.button("添加材料", type="primary"):
            if name and total_weight > 0:
                cost_per_gram = (purchase_price + shipping_fee) / total_weight
                # 保存图片
                image_path = None
                if uploaded_image is not None:
                    image_path = save_uploaded_image(uploaded_image, MATERIALS_IMAGES_DIR, name)
                    if image_path:
                        image_path = os.path.basename(image_path)
                new_row = pd.DataFrame([{
                    '名称': name,
                    '品牌': brand,
                    '质感': texture,
                    '耗材颜色': color,
                    '耗材类型': material_type,
                    '购买价': purchase_price,
                    '运费': shipping_fee,
                    '总克重': total_weight,
                    '购买时间': purchase_date,
                    '每克成本': cost_per_gram,
                    '图片路径': image_path,
                    '链接': link,
                    '备注': remark
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df, PRINT_MATERIALS_FILE)
                st.success(f"成功添加材料: {name}")
                st.rerun()
            else:
                st.error("请填写完整信息且总克重大于0")
    
    # 显示现有材料
    if not df.empty:
        st.subheader("现有材料")
        st.dataframe(df, use_container_width=True)
        st.subheader("编辑材料")
        for index, row in df.iterrows():
            with st.expander(f"{row['名称']} - 每克成本: ¥{row['每克成本']:.4f}"):
                if '图片路径' in row and row['图片路径']:
                    image_path = get_image_path(MATERIALS_IMAGES_DIR, row['图片路径'])
                    display_image(image_path, width=150)
                col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
                with col1:
                    new_name = st.text_input(f"名称_{index}", value=row['名称'], key=f"name_{index}")
                with col2:
                    new_brand = st.text_input(f"品牌_{index}", value=row.get('品牌', ''), key=f"brand_{index}")
                with col3:
                    new_texture = st.text_input(f"质感_{index}", value=row.get('质感', ''), key=f"texture_{index}")
                with col4:
                    new_color = st.text_input(f"耗材颜色_{index}", value=row.get('耗材颜色', ''), key=f"color_{index}")
                with col5:
                    new_material_type = st.text_input(f"耗材类型_{index}", value=row.get('耗材类型', ''), key=f"type_{index}")
                with col6:
                    new_purchase_price = st.number_input(f"购买价_{index}", value=row['购买价'], key=f"price_{index}")
                    new_shipping_fee = st.number_input(f"运费_{index}", value=row['运费'], key=f"shipping_{index}")
                with col7:
                    new_total_weight = st.number_input(f"总克重_{index}", value=row['总克重'], key=f"weight_{index}")
                    new_purchase_date = st.date_input(f"购买时间_{index}", value=row['购买时间'], key=f"date_{index}")
                with col8:
                    new_image = st.file_uploader(f"更新图片_{index}", type=['jpg', 'jpeg', 'png', 'gif'], key=f"material_update_{index}")
                new_link = st.text_input(f"链接_{index}", value=row.get('链接', ''), key=f"link_{index}")
                new_remark = st.text_area(f"备注_{index}", value=row.get('备注', ''), key=f"remark_{index}")
                if st.button(f"更新_{index}", key=f"update_{index}"):
                    if new_name and new_total_weight > 0:
                        new_cost_per_gram = (new_purchase_price + new_shipping_fee) / new_total_weight
                        new_image_path = row.get('图片路径', '')
                        if new_image is not None:
                            new_image_path = save_uploaded_image(new_image, MATERIALS_IMAGES_DIR, new_name)
                            if new_image_path:
                                new_image_path = os.path.basename(new_image_path)
                        df.loc[index] = [new_name, new_brand, new_texture, new_color, new_material_type, new_purchase_price, new_shipping_fee, new_total_weight, new_purchase_date, new_cost_per_gram, new_image_path, new_link, new_remark]
                        save_data(df, PRINT_MATERIALS_FILE)
                        st.success("更新成功")
                        st.rerun()
                    else:
                        st.error("请填写完整信息且总克重大于0")
                if st.button(f"删除_{index}", key=f"delete_{index}"):
                    if '图片路径' in row and row['图片路径']:
                        image_path = get_image_path(MATERIALS_IMAGES_DIR, row['图片路径'])
                        if image_path and os.path.exists(image_path):
                            os.remove(image_path)
                    df = df.drop(index)
                    save_data(df, PRINT_MATERIALS_FILE)
                    st.success("删除成功")
                    st.rerun()
    else:
        st.info("暂无材料数据，请添加新材料")

def show_accessories_page():
    st.header("🔧 产品配件管理")
    
    # 加载数据
    df = load_data(ACCESSORIES_FILE)
    
    # 如果没有数据，创建空的DataFrame
    if df.empty:
        df = pd.DataFrame(columns=['名称', '规格', '购买价', '运费', '总数量', '购买时间', '每单位成本', '图片路径', '链接', '备注'])
    # 补全旧数据缺失的列
    for col in ['规格', '链接', '备注']:
        if col not in df.columns:
            df[col] = ''
    
    # 添加新配件的表单
    with st.expander("添加新配件", expanded=True):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            name = st.text_input("名称", key="acc_name")
        with col2:
            spec = st.text_input("规格", key="acc_spec")
        with col3:
            purchase_price = st.number_input("购买价 (元)", min_value=0.0, value=0.0, step=0.01, key="acc_price")
        with col4:
            shipping_fee = st.number_input("运费 (元)", min_value=0.0, value=0.0, step=0.01, key="acc_shipping")
            total_quantity = st.number_input("总数量", min_value=1, value=1, step=1, key="acc_quantity")
        with col5:
            purchase_date = st.date_input("购买时间", value=datetime.now(), key="acc_date")
        link = st.text_input("链接", placeholder="购买链接或产品链接", key="acc_link")
        remark = st.text_area("备注", placeholder="额外说明信息", key="acc_remark")
        uploaded_image = st.file_uploader("上传图片", type=['jpg', 'jpeg', 'png', 'gif'], key="accessory_upload")
        if st.button("添加配件", type="primary", key="acc_add"):
            if name and total_quantity > 0:
                cost_per_unit = (purchase_price + shipping_fee) / total_quantity
                image_path = None
                if uploaded_image is not None:
                    image_path = save_uploaded_image(uploaded_image, ACCESSORIES_IMAGES_DIR, name)
                    if image_path:
                        image_path = os.path.basename(image_path)
                new_row = pd.DataFrame([{
                    '名称': name,
                    '规格': spec,
                    '购买价': purchase_price,
                    '运费': shipping_fee,
                    '总数量': total_quantity,
                    '购买时间': purchase_date,
                    '每单位成本': cost_per_unit,
                    '图片路径': image_path,
                    '链接': link,
                    '备注': remark
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df, ACCESSORIES_FILE)
                st.success(f"成功添加配件: {name}")
                st.rerun()
            else:
                st.error("请填写完整信息且总数量大于0")
    
    # 显示现有配件
    if not df.empty:
        st.subheader("现有配件")
        st.dataframe(df, use_container_width=True)
        st.subheader("编辑配件")
        for index, row in df.iterrows():
            with st.expander(f"{row['名称']} - 每单位成本: ¥{row['每单位成本']:.2f}"):
                if '图片路径' in row and row['图片路径']:
                    image_path = get_image_path(ACCESSORIES_IMAGES_DIR, row['图片路径'])
                    display_image(image_path, width=150)
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    new_name = st.text_input(f"名称_{index}", value=row['名称'], key=f"acc_name_{index}")
                with col2:
                    new_spec = st.text_input(f"规格_{index}", value=row.get('规格', ''), key=f"acc_spec_{index}")
                with col3:
                    new_purchase_price = st.number_input(f"购买价_{index}", value=row['购买价'], key=f"acc_price_{index}")
                    new_shipping_fee = st.number_input(f"运费_{index}", value=row['运费'], key=f"acc_shipping_{index}")
                with col4:
                    new_total_quantity = st.number_input(f"总数量_{index}", value=row['总数量'], key=f"acc_quantity_{index}")
                    new_purchase_date = st.date_input(f"购买时间_{index}", value=row['购买时间'], key=f"acc_date_{index}")
                with col5:
                    new_image = st.file_uploader(f"更新图片_{index}", type=['jpg', 'jpeg', 'png', 'gif'], key=f"accessory_update_{index}")
                new_link = st.text_input(f"链接_{index}", value=row.get('链接', ''), key=f"acc_link_{index}")
                new_remark = st.text_area(f"备注_{index}", value=row.get('备注', ''), key=f"acc_remark_{index}")
                if st.button(f"更新_{index}", key=f"acc_update_{index}"):
                    if new_name and new_total_quantity > 0:
                        new_cost_per_unit = (new_purchase_price + new_shipping_fee) / new_total_quantity
                        new_image_path = row.get('图片路径', '')
                        if new_image is not None:
                            new_image_path = save_uploaded_image(new_image, ACCESSORIES_IMAGES_DIR, new_name)
                            if new_image_path:
                                new_image_path = os.path.basename(new_image_path)
                        df.loc[index] = [new_name, new_spec, new_purchase_price, new_shipping_fee, new_total_quantity, new_purchase_date, new_cost_per_unit, new_image_path, new_link, new_remark]
                        save_data(df, ACCESSORIES_FILE)
                        st.success("更新成功")
                        st.rerun()
                    else:
                        st.error("请填写完整信息且总数量大于0")
                if st.button(f"删除_{index}", key=f"acc_delete_{index}"):
                    if '图片路径' in row and row['图片路径']:
                        image_path = get_image_path(ACCESSORIES_IMAGES_DIR, row['图片路径'])
                        if image_path and os.path.exists(image_path):
                            os.remove(image_path)
                    df = df.drop(index)
                    save_data(df, ACCESSORIES_FILE)
                    st.success("删除成功")
                    st.rerun()
    else:
        st.info("暂无配件数据，请添加新配件")

def show_packaging_page():
    st.header("📦 包装管理")
    
    # 加载数据
    df = load_data(PACKAGING_FILE)
    
    # 如果没有数据，创建空的DataFrame
    if df.empty:
        df = pd.DataFrame(columns=['名称', '规格', '购买价', '运费', '总数量', '购买时间', '每单位成本', '图片路径', '链接', '备注'])
    for col in ['规格', '链接', '备注']:
        if col not in df.columns:
            df[col] = ''
    
    # 添加新包装的表单
    with st.expander("添加新包装", expanded=True):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            name = st.text_input("名称", key="pkg_name")
        with col2:
            spec = st.text_input("规格", key="pkg_spec")
        with col3:
            purchase_price = st.number_input("购买价 (元)", min_value=0.0, value=0.0, step=0.01, key="pkg_price")
        with col4:
            shipping_fee = st.number_input("运费 (元)", min_value=0.0, value=0.0, step=0.01, key="pkg_shipping")
            total_quantity = st.number_input("总数量", min_value=1, value=1, step=1, key="pkg_quantity")
        with col5:
            purchase_date = st.date_input("购买时间", value=datetime.now(), key="pkg_date")
        link = st.text_input("链接", placeholder="购买链接或产品链接", key="pkg_link")
        remark = st.text_area("备注", placeholder="额外说明信息", key="pkg_remark")
        uploaded_image = st.file_uploader("上传图片", type=['jpg', 'jpeg', 'png', 'gif'], key="packaging_upload")
        if st.button("添加包装", type="primary", key="pkg_add"):
            if name and total_quantity > 0:
                cost_per_unit = (purchase_price + shipping_fee) / total_quantity
                image_path = None
                if uploaded_image is not None:
                    image_path = save_uploaded_image(uploaded_image, PACKAGING_IMAGES_DIR, name)
                    if image_path:
                        image_path = os.path.basename(image_path)
                new_row = pd.DataFrame([{
                    '名称': name,
                    '规格': spec,
                    '购买价': purchase_price,
                    '运费': shipping_fee,
                    '总数量': total_quantity,
                    '购买时间': purchase_date,
                    '每单位成本': cost_per_unit,
                    '图片路径': image_path,
                    '链接': link,
                    '备注': remark
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df, PACKAGING_FILE)
                st.success(f"成功添加包装: {name}")
                st.rerun()
            else:
                st.error("请填写完整信息且总数量大于0")
    
    # 显示现有包装
    if not df.empty:
        st.subheader("现有包装")
        st.dataframe(df, use_container_width=True)
        st.subheader("编辑包装")
        for index, row in df.iterrows():
            with st.expander(f"{row['名称']} - 每单位成本: ¥{row['每单位成本']:.2f}"):
                if '图片路径' in row and row['图片路径']:
                    image_path = get_image_path(PACKAGING_IMAGES_DIR, row['图片路径'])
                    display_image(image_path, width=150)
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    new_name = st.text_input(f"名称_{index}", value=row['名称'], key=f"pkg_name_{index}")
                with col2:
                    new_spec = st.text_input(f"规格_{index}", value=row.get('规格', ''), key=f"pkg_spec_{index}")
                with col3:
                    new_purchase_price = st.number_input(f"购买价_{index}", value=row['购买价'], key=f"pkg_price_{index}")
                    new_shipping_fee = st.number_input(f"运费_{index}", value=row['运费'], key=f"pkg_shipping_{index}")
                with col4:
                    new_total_quantity = st.number_input(f"总数量_{index}", value=row['总数量'], key=f"pkg_quantity_{index}")
                    new_purchase_date = st.date_input(f"购买时间_{index}", value=row['购买时间'], key=f"pkg_date_{index}")
                with col5:
                    new_image = st.file_uploader(f"更新图片_{index}", type=['jpg', 'jpeg', 'png', 'gif'], key=f"pkg_image_{index}")
                new_link = st.text_input(f"链接_{index}", value=row.get('链接', ''), key=f"pkg_link_{index}")
                new_remark = st.text_area(f"备注_{index}", value=row.get('备注', ''), key=f"pkg_remark_{index}")
                if st.button(f"更新_{index}", key=f"pkg_update_btn_{index}"):
                    if new_name and new_total_quantity > 0:
                        new_cost_per_unit = (new_purchase_price + new_shipping_fee) / new_total_quantity
                        new_image_path = row.get('图片路径', '')
                        if new_image is not None:
                            new_image_path = save_uploaded_image(new_image, PACKAGING_IMAGES_DIR, new_name)
                            if new_image_path:
                                new_image_path = os.path.basename(new_image_path)
                        df.loc[index] = [new_name, new_spec, new_purchase_price, new_shipping_fee, new_total_quantity, new_purchase_date, new_cost_per_unit, new_image_path, new_link, new_remark]
                        save_data(df, PACKAGING_FILE)
                        st.success("更新成功")
                        st.rerun()
                    else:
                        st.error("请填写完整信息且总数量大于0")
                if st.button(f"删除_{index}", key=f"pkg_delete_btn_{index}"):
                    if '图片路径' in row and row['图片路径']:
                        image_path = get_image_path(PACKAGING_IMAGES_DIR, row['图片路径'])
                        if image_path and os.path.exists(image_path):
                            os.remove(image_path)
                    df = df.drop(index)
                    save_data(df, PACKAGING_FILE)
                    st.success("删除成功")
                    st.rerun()
    else:
        st.info("暂无包装数据，请添加新包装")

if __name__ == "__main__":
    main() 