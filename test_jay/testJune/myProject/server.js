const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors'); // CORS 미들웨어 추가
const fs = require('fs');
const path = require('path');

const app = express();
app.use(bodyParser.json());

// 모든 출처에서의 요청을 허용
app.use(cors());

// 클라이언트로부터 받은 데이터를 저장하는 엔드포인트
app.post('/save_data', (req, res) => {
    const data = req.body;

    const dirPath = path.join(__dirname, 'data');
    const filePath = path.join(dirPath, '1.json');

    if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath);
    }

    fs.writeFile(filePath, JSON.stringify(data, null, 2), (err) => {
        if (err) {
            console.error('파일 저장 중 오류 발생:', err);
            return res.status(500).send('파일 저장 중 오류 발생');
        }
        console.log('상담 내용이 성공적으로 저장되었습니다.');
        res.status(200).send('성공적으로 저장되었습니다.');
    });
});

// JSON 데이터를 제공하는 엔드포인트
app.get('/get_data', (req, res) => {
    const filePath = path.join(__dirname, 'data', '1.json');

    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error('파일 읽기 중 오류 발생:', err);
            return res.status(500).send('파일 읽기 중 오류 발생');
        }
        res.status(200).json(JSON.parse(data));
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`서버가 http://localhost:${PORT} 에서 실행 중입니다.`);
});
