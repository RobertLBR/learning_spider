from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import os
import time
import logging
import shutil
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 启用CORS支持

# 记录应用启动时间
app.config['START_TIME'] = time.time()

# 应用配置
app.config.update(
    MAX_CONTENT_LENGTH=10 * 1024 * 1024,  # 限制上传文件大小为10MB
    UPLOAD_FOLDER=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp'),
    MAX_TEMP_FILE_AGE=3600,  # 临时文件最大保存时间（秒）
    ALLOWED_EXTENSIONS=ALLOWED_EXTENSIONS,
    DEBUG=False,  # 生产环境禁用调试模式
    JSON_AS_ASCII=False,  # 支持JSON中的中文字符
    JSON_SORT_KEYS=True,  # 对JSON响应的键进行排序
)

# 安全配置
app.config.update(
    SESSION_COOKIE_SECURE=True,  # 仅通过HTTPS发送cookie
    SESSION_COOKIE_HTTPONLY=True,  # 防止JavaScript访问cookie
    SESSION_COOKIE_SAMESITE='Lax',  # 防止CSRF攻击
    PERMANENT_SESSION_LIFETIME=1800,  # 会话超时时间（秒）
)

# 配置请求限制
app.config.update(
    MAX_REQUESTS_PER_MINUTE=60,  # 每分钟最大请求数
    MAX_REQUESTS_PER_HOUR=1000,  # 每小时最大请求数
)

# 配置上传文件的临时目录
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    logger.info(f"创建临时目录: {UPLOAD_FOLDER}")

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 清理超过1小时的临时文件
def cleanup_temp_files():
    try:
        current_time = time.time()
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            # 如果文件或目录的最后修改时间超过1小时
            if os.path.isfile(file_path) and (current_time - os.path.getmtime(file_path)) > 3600:
                os.remove(file_path)
                logger.info(f"已删除过期临时文件: {filename}")
    except Exception as e:
        logger.error(f"清理临时文件时出错: {str(e)}")

# 错误处理
@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    logger.warning("上传文件过大")
    return jsonify({'error': '文件大小超过限制（最大10MB）'}), 413

@app.errorhandler(404)
def handle_not_found(e):
    return jsonify({'error': '找不到请求的资源'}), 404

@app.errorhandler(500)
def handle_server_error(e):
    logger.error(f"服务器错误: {str(e)}")
    return jsonify({'error': '服务器内部错误'}), 500

# 添加根路径处理
@app.route('/', methods=['GET'])
def index():
    # 提供一个简单的HTML页面，说明这是API服务器
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>图片背景消除工具 - API服务器</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }
            h1 {
                color: #2196F3;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
            }
            .info {
                background-color: #f8f9fa;
                border-left: 4px solid #17a2b8;
                padding: 15px;
                margin: 20px 0;
                border-radius: 4px;
            }
            .warning {
                background-color: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 20px 0;
                border-radius: 4px;
            }
            code {
                background-color: #f1f1f1;
                padding: 2px 5px;
                border-radius: 3px;
                font-family: monospace;
            }
            .endpoint {
                margin: 20px 0;
                background-color: #ffffff;
                padding: 15px;
                border-radius: 4px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .endpoint h3 {
                margin-bottom: 5px;
                color: #333;
            }
            .method {
                display: inline-block;
                padding: 3px 6px;
                background-color: #4CAF50;
                color: white;
                border-radius: 3px;
                font-size: 0.8em;
                margin-right: 5px;
            }
            .method.post {
                background-color: #2196F3;
            }
            .status {
                margin-top: 20px;
                padding: 10px;
                background-color: #e8f5e9;
                border-radius: 4px;
                text-align: center;
            }
            footer {
                margin-top: 30px;
                text-align: center;
                color: #666;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <h1>图片背景消除工具 - API服务器</h1>
        
        <div class="info">
            <p>这是图片背景消除工具的后端API服务器。请不要直接访问此地址，而是通过前端应用使用此服务。</p>
            <p>前端应用地址: <code>http://localhost:3000</code></p>
        </div>
        
        <div class="warning">
            <p><strong>注意:</strong> 此服务器仅处理图片背景移除请求，不提供用户界面。</p>
        </div>
        
        <h2>API端点</h2>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> 移除图片背景</h3>
            <p><code>/api/remove-bg</code></p>
            <p>上传图片并移除背景。</p>
            <p><strong>请求格式:</strong> multipart/form-data</p>
            <p><strong>参数:</strong> image (文件)</p>
            <p><strong>支持格式:</strong> PNG, JPG, JPEG, GIF, WebP</p>
            <p><strong>大小限制:</strong> 10MB</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> 健康检查</h3>
            <p><code>/api/health</code></p>
            <p>检查API服务器是否正常运行。</p>
            <p><strong>返回:</strong> JSON格式的服务器状态信息</p>
        </div>
        
        <div class="status">
            <p>服务器状态: <strong>运行中</strong></p>
        </div>
        
        <footer>
            <p>图片背景消除工具 &copy; 2023 | 基于Flask和Rembg开发</p>
        </footer>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/api/remove-bg', methods=['POST'])
def remove_background():
    start_time = time.time()
    logger.info("收到背景移除请求")
    
    try:
        # 检查是否有文件被上传
        if 'image' not in request.files:
            logger.warning("未提供图片")
            return jsonify({'error': '没有上传文件'}), 400
        
        file = request.files['image']
        
        # 检查文件名是否为空
        if file.filename == '':
            logger.warning("未选择图片")
            return jsonify({'error': '没有选择文件'}), 400
        
        # 检查文件类型
        if not allowed_file(file.filename):
            logger.warning(f"不支持的文件类型: {file.filename}")
            return jsonify({'error': '不支持的文件类型，请上传PNG、JPG、JPEG、GIF或WebP格式的图片'}), 400

        # 读取上传的图片
        input_image = Image.open(file.stream)
        
        # 记录图片信息
        img_format = input_image.format
        img_size = input_image.size
        logger.info(f"处理图片: 格式={img_format}, 尺寸={img_size[0]}x{img_size[1]}")
        
        # 处理图片
        logger.info("开始移除背景")
        output_image = remove(input_image)
        logger.info("背景移除完成")
        
        # 保存处理后的图片到临时文件（用于调试和审计）
        try:
            filename = secure_filename(file.filename)
            output_path = os.path.join(UPLOAD_FOLDER, f"processed_{filename.split('.')[0]}_{int(time.time())}.png")
            output_image.save(output_path)
            logger.info(f"已保存处理后的图片: {output_path}")
        except Exception as save_error:
            logger.warning(f"保存临时文件失败: {str(save_error)}")
            # 继续处理，不中断流程
        
        # 将处理后的图片转换为bytes
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # 计算处理时间
        process_time = time.time() - start_time
        logger.info(f"处理完成，耗时: {process_time:.2f}秒")
        
        # 返回处理后的图片
        return send_file(
            img_byte_arr,
            mimetype='image/png',
            as_attachment=True,
            download_name='removed_bg.png'
        )

    except Exception as e:
        logger.error(f"处理图片时出错: {str(e)}", exc_info=True)
        return jsonify({'error': f'处理图片时出错: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    # 清理过期的临时文件
    cleanup_temp_files()
    
    # 检查临时目录是否存在
    temp_dir_exists = os.path.exists(UPLOAD_FOLDER)
    
    # 检查是否可以创建文件
    can_write = False
    try:
        test_file = os.path.join(UPLOAD_FOLDER, 'test_write.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        can_write = True
    except Exception as e:
        logger.warning(f"写入测试失败: {str(e)}")
    
    # 检查rembg是否可用
    rembg_available = True
    try:
        test_img = Image.new('RGB', (10, 10), color='red')
        remove(test_img)
    except Exception as e:
        logger.error(f"Rembg测试失败: {str(e)}")
        rembg_available = False
    
    status = 'healthy' if (temp_dir_exists and can_write and rembg_available) else 'unhealthy'
    
    response = {
        'status': status,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'checks': {
            'temp_directory': temp_dir_exists,
            'write_permission': can_write,
            'rembg_available': rembg_available
        },
        'version': '1.0.0',
        'uptime': time.time() - app.config.get('START_TIME', time.time())
    }
    
    return jsonify(response), 200 if status == 'healthy' else 503

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)