import axios from '../utils/axios';

/**
 * 文件上传接口
 * @param {File} file - 要上传的文件
 * @param {number} project_id - 项目ID
 * @param {string} type - 文件类型
 * @returns {Promise<any>}
 */
export const uploadIcon = (file) => {
  const formData = new FormData();
  formData.append('file', file);
//   formData.append('project_id', project_id);
  formData.append('type', 'icon');

  return axios.post('/file/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

/**
 * 图片预览接口
 * @param {string} image_name - 图片名称
 * @returns {Promise<any>}
 */
export const previewImage = (image_name) => {
  return axios.get(`/file/image/preview/${image_name}`);
};