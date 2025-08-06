import React, { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';
import './App.css';

// 处理进度状态常量
const PROCESS_STATES = {
  IDLE: 'idle',
  UPLOADING: 'uploading',
  PROCESSING: 'processing',
  COMPLETED: 'completed',
  ERROR: 'error'
};

// 进度指示器组件
const ProgressIndicator = ({ state, progress }) => {
  const getStateMessage = () => {
    switch (state) {
      case PROCESS_STATES.UPLOADING:
        return `上传中 ${progress}%`;
      case PROCESS_STATES.PROCESSING:
        return '处理中...';
      case PROCESS_STATES.COMPLETED:
        return '处理完成！';
      case PROCESS_STATES.ERROR:
        return '处理出错';
      default:
        return '';
    }
  };

  if (state === PROCESS_STATES.IDLE) return null;

  return (
    <div className={`progress-indicator ${state}`}>
      <div className="progress-bar" style={{ width: `${progress}%` }}></div>
      <span className="progress-text">{getStateMessage()}</span>
    </div>
  );
};

// 图片预览放大组件
const ImageLightbox = ({ imageUrl, onClose }) => {
  if (!imageUrl) return null;
  
  return (
    <div className="lightbox-overlay" onClick={onClose}>
      <div className="lightbox-content" onClick={e => e.stopPropagation()}>
        <button className="lightbox-close" onClick={onClose}>×</button>
        <img src={imageUrl} alt="放大预览" className="lightbox-image" />
      </div>
    </div>
  );
};

function App() {
  const [originalImage, setOriginalImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [backendStatus, setBackendStatus] = useState('checking');
  const [uploadFile, setUploadFile] = useState(null);
  const [processState, setProcessState] = useState(PROCESS_STATES.IDLE);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const [showLightbox, setShowLightbox] = useState(false);
  const [lightboxImage, setLightboxImage] = useState(null);
  const [processingOptions, setProcessingOptions] = useState({
    alpha_matting: false,
    alpha_matting_foreground_threshold: 240,
    alpha_matting_background_threshold: 10,
    alpha_matting_erode_size: 10
  });
  
  const fileInputRef = useRef(null);
  const dropZoneRef = useRef(null);

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

  // 拖拽相关处理函数
  const handleDragEnter = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.target === dropZoneRef.current) {
      setIsDragging(false);
    }
  }, []);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  }, []);

  // 统一的文件处理函数
  const handleFileSelect = (file) => {
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
      setProcessState(PROCESS_STATES.IDLE);
      setUploadProgress(0);
    };
    reader.readAsDataURL(file);
    setUploadFile(file);
  };

  // 处理图片上传
  const handleImageUpload = (event) => {
    handleFileSelect(event.target.files[0]);
  };

  // 图片预览功能
  const openLightbox = useCallback((imageUrl) => {
    setLightboxImage(imageUrl);
    setShowLightbox(true);
  }, []);

  const closeLightbox = useCallback(() => {
    setShowLightbox(false);
  }, []);

  // 处理参数变更
  const handleOptionChange = (option, value) => {
    setProcessingOptions(prev => ({
      ...prev,
      [option]: value
    }));
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
    setProcessState(PROCESS_STATES.UPLOADING);
    setUploadProgress(0);

    try {
      // 创建FormData对象
      const formData = new FormData();
      formData.append('image', uploadFile);
      
      // 添加处理参数
      Object.entries(processingOptions).forEach(([key, value]) => {
        formData.append(key, value);
      });

      // 发送请求到后端API
      const response = await axios.post('/api/remove-bg', formData, {
        responseType: 'blob',
        timeout: 120000, // 120秒超时
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setUploadProgress(percentCompleted);
          
          if (percentCompleted === 100) {
            setProcessState(PROCESS_STATES.PROCESSING);
          }
        }
      });

      // 处理返回的图片blob
      const processedBlob = new Blob([response.data], { type: 'image/png' });
      const imageUrl = URL.createObjectURL(processedBlob);
      setProcessedImage(imageUrl);
      setProcessState(PROCESS_STATES.COMPLETED);
    } catch (err) {
      console.error('去除背景失败:', err);
      setProcessState(PROCESS_STATES.ERROR);
      
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
        <div 
          ref={dropZoneRef}
          className={`upload-section ${isDragging ? 'dragging' : ''}`}
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          <input
            type="file"
            ref={fileInputRef}
            accept="image/jpeg,image/png,image/gif,image/webp"
            onChange={handleImageUpload}
            className="file-input"
          />
          <label 
            onClick={() => fileInputRef.current.click()}
            className="upload-button"
          >
            选择图片
          </label>
          <p className="drag-hint">或将图片拖放到此处</p>
        </div>

        {error && <div className="error-message">{error}</div>}
        
        <ProgressIndicator state={processState} progress={uploadProgress} />

        {originalImage && (
          <div className="processing-options">
            <h3>处理参数</h3>
            <div className="option-group">
              <label>
                <input
                  type="checkbox"
                  checked={processingOptions.alpha_matting}
                  onChange={(e) => handleOptionChange('alpha_matting', e.target.checked)}
                />
                启用 Alpha Matting
              </label>
              {processingOptions.alpha_matting && (
                <>
                  <div className="slider-group">
                    <label>前景阈值</label>
                    <input
                      type="range"
                      min="0"
                      max="255"
                      value={processingOptions.alpha_matting_foreground_threshold}
                      onChange={(e) => handleOptionChange('alpha_matting_foreground_threshold', parseInt(e.target.value))}
                    />
                    <span>{processingOptions.alpha_matting_foreground_threshold}</span>
                  </div>
                  <div className="slider-group">
                    <label>背景阈值</label>
                    <input
                      type="range"
                      min="0"
                      max="255"
                      value={processingOptions.alpha_matting_background_threshold}
                      onChange={(e) => handleOptionChange('alpha_matting_background_threshold', parseInt(e.target.value))}
                    />
                    <span>{processingOptions.alpha_matting_background_threshold}</span>
                  </div>
                  <div className="slider-group">
                    <label>边缘大小</label>
                    <input
                      type="range"
                      min="0"
                      max="50"
                      value={processingOptions.alpha_matting_erode_size}
                      onChange={(e) => handleOptionChange('alpha_matting_erode_size', parseInt(e.target.value))}
                    />
                    <span>{processingOptions.alpha_matting_erode_size}</span>
                  </div>
                </>
              )}
            </div>
            
            <button 
              className="process-button" 
              onClick={handleRemoveBackground}
              disabled={!originalImage || loading || backendStatus !== 'connected'}
            >
              {loading ? '处理中...' : '去除背景'}
            </button>
          </div>
        )}

        <div className="image-preview-container">
          <div className="image-preview">
            <h3>原始图片</h3>
            {originalImage && (
              <img 
                src={originalImage} 
                alt="Original" 
                className="preview-image" 
                onClick={() => openLightbox(originalImage)}
              />
            )}
          </div>

          <div className="image-preview">
            <h3>处理后图片</h3>
            {processedImage && (
              <>
                <img 
                  src={processedImage} 
                  alt="Processed" 
                  className="preview-image" 
                  onClick={() => openLightbox(processedImage)}
                />
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

      {showLightbox && (
        <ImageLightbox
          imageUrl={lightboxImage}
          onClose={closeLightbox}
        />
      )}
    </div>
  );
}

export default App;