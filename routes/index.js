var express = require('express');
var router = express.Router();
const { exec } = require('child_process');
require('dotenv').config();
const { GoogleGenerativeAI } = require("@google/generative-ai");


const genAI = new GoogleGenerativeAI(process.env.API_KEY); // Initialize with your API key
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" }); // Set the model


const { createCanvas } = require('canvas');
const fs = require('fs');


/* GET home page. */
router.get('/', function (req, res, next) {
    res.render('index');
});

router.get('/result', function (req, res, next) {
    res.render('result', { pythonScriptOutput: '' });
});

router.post('/result', async function (req, res, next) {
    const url = req.body.url;
    const scriptPath = './main.py';
    const command = `python "${scriptPath}" "${url}"`;

    try {
        const stdout = await new Promise((resolve, reject) => {
            exec(command, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error executing Python script: ${error}`);
                    reject(error);
                } else {
                    resolve(stdout);
                }
            });
        });

        const pythonData = JSON.parse(stdout);
        const {
            positive_table,
            neutral_table,
            negative_table,
            countTotal,
            countPositive,
            countNeutral,
            countNegative,
            positive_list,
            neutral_list,
            negative_list,
            allComments
        } = pythonData;

        console.log("Python script executed successfully, output variables generated");

        // Generate Pie Chart
        createPieChart(countPositive, countNeutral, countNegative);

        const topicsPrompt = `These are comments on my YouTube video:\n${allComments.join('\n')}\n\nAnalyze these comments and extract 10-15 topics and video ideas that my viewers are asking for in the comments. Give each idea in a numbered list and keep the response to the point.`;
        const critisismPrompt = `These are comments on my YouTube video:\n${allComments.join('\n')}\n\nAnalyze these comments and extract genuine criticism or improvements based on the comments received. Give each criticism in a numbered list and keep the response to the point.`;
        const qnaPrompt = `These are comments on my YouTube video:\n${allComments.join('\n')}\n\nAnalyze these comments and extract 10-15 repeatedly asked questions from the comments. Only questions, no answers needed. Give each question in a numbered list and keep the response to the point.`;

        const prompts = [topicsPrompt, critisismPrompt, qnaPrompt];

        // Generate responses using Gemini API
        const responses = await Promise.all(
            prompts.map(async (prompt) => {
                const result = await model.generateContent(prompt);
                return result.response.text(); // Access the text response
            })
        );

        let topics_response = responses[0];
        let critisism_response = responses[1];
        let qna_response = responses[2];

        if (topics_response != null || critisism_response != null || qna_response != null) {
            topics_response = topics_response.replace(/\*/g, ''); // Remove asterisks
            critisism_response = critisism_response.replace(/\*/g, ''); // Remove asterisks
            qna_response = qna_response.replace(/\*/g, ''); // Remove asterisks
        }

        console.log(topics_response, critisism_response, qna_response);

        res.render('result', {
            pythonScriptOutput: stdout,
            positive_table,
            negative_table,
            neutral_table,
            countTotal,
            countPositive,
            countNeutral,
            countNegative,
            positive_list,
            neutral_list,
            negative_list,
            topics: topics_response,
            critisism: critisism_response,
            qna: qna_response
        });

    } catch (error) {
        console.error('Error:', error);
        res.status(500).send("Internal Server Error");
    }
});

// Function to create a pie chart and save it as an image
function createPieChart(countPositive, countNeutral, countNegative) {
    const canvas = createCanvas(300, 300); // Create a 300x300 canvas
    const ctx = canvas.getContext('2d');

    const total = countPositive + countNeutral + countNegative;
    const positivePercentage = (countPositive / total) * 100 || 0;
    const neutralPercentage = (countNeutral / total) * 100 || 0;
    const negativePercentage = (countNegative / total) * 100 || 0;

    // Define colors for the segments
    const hex_colors = ['#AEE2FF', '#FF6969', '#FEFF86'];
    const percentages = [positivePercentage, neutralPercentage, negativePercentage];

    let startAngle = 0;

    percentages.forEach((percentage, index) => {
        const sliceAngle = (percentage / 100) * (Math.PI * 2);
        ctx.beginPath();
        ctx.moveTo(150, 150); // Center of the pie
        ctx.arc(150, 150, 150, startAngle, startAngle + sliceAngle); // Draw pie slice
        ctx.fillStyle = hex_colors[index]; // Set fill color
        ctx.fill();
        startAngle += sliceAngle; // Update start angle for next slice

        // Calculate the angle to position the percentage text
        const textAngle = startAngle - sliceAngle / 2;
        const textX = 150 + (75 * Math.cos(textAngle)); // Adjusted radius for text position
        const textY = 150 + (75 * Math.sin(textAngle)); // Adjusted radius for text position
        ctx.fillStyle = 'black';
        ctx.font = '16px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`${Math.round(percentage)}%`, textX, textY); // Draw percentage in the segment
    });

    // Save the pie chart as an image in the root directory
    const buffer = canvas.toBuffer('image/png');
    fs.writeFileSync('./sentiment_pie_chart.png', buffer);
    console.log('Sentiment pie chart saved as sentiment_pie_chart.png');
}



module.exports = router;