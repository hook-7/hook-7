import axios from 'axios'

// 创建axios实例
const service = axios.create({
  // axios中请求配置有baseURL选项，表示请求URL公共部分
  baseURL: import.meta.env.VITE_API_BASE_URL

})
console.log(import.meta.env.VITE_API_BASE_URL);
export default service