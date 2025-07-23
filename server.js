const express = require('express');
const { Pool } = require('pg');
const path = require('path');
const app = express();
require('dotenv').config();

// PostgreSQL 连接配置
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

// 测试数据库连接
pool.query('SELECT NOW()', (err, res) => {
  if (err) {
    console.error('❌ 数据库连接失败:', err.stack);
  } else {
    console.log('✅ 数据库连接成功:', res.rows[0].now);
  }
});

// 中间件
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// API路由 - 获取媒体数据
app.get('/api/media', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM media ORDER BY id');
    res.json(result.rows);
  } catch (err) {
    console.error('❌ 查询媒体数据失败:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// API路由 - 获取用户评价
app.get('/api/testimonials', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM testimonials ORDER BY rating DESC');
    res.json(result.rows);
  } catch (err) {
    console.error('❌ 查询用户评价失败:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// 启动服务器
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🌐 Server running on port ${PORT}`);
});