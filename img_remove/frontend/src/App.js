import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [originalImage, setOriginalImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [backendStatus, setBackendStatus] = useState('checking');
  const [uploadFile, setUploadFile] = useState(null);

  // 检查后端服务状态
  useEffect(() => {
    const checkBackendStatus = async () => {
      try {
        await axios.get('/api/health');
        setBackendStatus('connected');
      } catch (err) {
        console.error('后端服务连接失败:', err);
        setBackendStatus('disconnected');
      }
    };

    checkBackendStatus();
    const intervalId = setInterval(checkBackendStatus, 30000); // 每30秒检查一次

    return () => clearInterval(intervalId);
  }, []);

  // 处理图片上传
  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // 检查文件类型
    const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      setError('请上传支持的图片格式（JPEG, PNG, GIF, WebP）');
      return;
    }

    // 检查文件大小（限制为10MB）
    if (file.size > 10 * 1024 * 1024) {
      setError('文件大小不能超过10MB');
      return;
    }

    // 显示原始图片预览
    const reader = new FileReader();
    reader.onload = (e) => {
      setOriginalImage(e.target.result);
      setProcessedImage(null); // 清除之前处理的图片
      setError(null);
    };
    reader.readAsDataURL(file);
    setUploadFile(file);
  };

  // 处理图片背景去除
  const handleRemoveBackground = async () => {
    if (!uploadFile) {
      setError('请先上传图片');
      return;
    }

    if (backendStatus !== 'connected') {
      setError('后端服务未连接，请确保服务正常运行');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // 创建FormData对象
      const formData = new FormData();
      formData.append('image', uploadFile);

      // 发送请求到后端API
      const response = await axios.post('/api/remove-bg', formData, {
        responseType: 'blob',
        timeout: 60000, // 60秒超时
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // 处理返回的图片blob
      const processedBlob = new Blob([response.data], { type: 'image/png' });
      const imageUrl = URL.createObjectURL(processedBlob);
      setProcessedImage(imageUrl);
    } catch (err) {
      console.error('去除背景失败:', err);
      if (err.code === 'ECONNABORTED') {
        setError('请求超时，请尝试处理小一点的图片');
      } else if (err.response) {
        setError(`处理失败: ${err.response.status} ${err.response.statusText}`);
      } else if (err.request) {
        setError('无法连接到服务器，请检查网络连接');
      } else {
        setError('处理图片时出错: ' + err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  // 下载处理后的图片
  const handleDownload = () => {
    if (!processedImage) return;

    const link = document.createElement('a');
    link.href = processedImage;
    link.download = 'removed_background.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // 清理URL对象
  useEffect(() => {
    return () => {
      if (processedImage) {
        URL.revokeObjectURL(processedImage);
      }
    };
  }, [processedImage]);

  return (
    <div className="app">
      <header className="app-header">
        <h1>图片背景消除工具</h1>
        <p>上传图片，一键去除背景</p>
        {backendStatus === 'disconnected' && (
          <div className="error-message">
            警告: 后端服务未连接，请确保服务正常运行
          </div>
        )}
      </header>

      <main className="app-main">
        <div className="upload-section">
          <input
            type="file"
            id="image-upload"
            accept="image/jpeg,image/png,image/gif,image/webp"
            onChange={handleImageUpload}
            className="file-input"
          />
          <label htmlFor="image-upload" className="upload-button">
            选择图片
          </label>
          
          <button 
            className="process-button" 
            onClick={handleRemoveBackground}
            disabled={!originalImage || loading || backendStatus !== 'connected'}
          >
            {loading ? '处理中...' : '去除背景'}
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="image-preview-container">
          <div className="image-preview">
            <h3>原始图片</h3>
            {originalImage && (
              <img src={originalImage} alt="Original" className="preview-image" />
            )}
          </div>

          <div className="image-preview">
            <h3>处理后图片</h3>
            {processedImage && (
              <>
                <img src={processedImage} alt="Processed" className="preview-image" />
                <button className="download-button" onClick={handleDownload}>
                  下载图片
                </button>
              </>
            )}
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>基于 React + Flask + Rembg 开发</p>
        <p>后端状态: {
          backendStatus === 'connected' ? '已连接' :
          backendStatus === 'checking' ? '检查中...' :
          '未连接'
        }</p>
      </footer>
    </div>
  );
}

export default App;