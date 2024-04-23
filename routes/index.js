var express = require('express');
var router = express.Router();
const { exec } = require('child_process');


const { G4F } = require("g4f");
const GPT = new G4F();

// -------------------------------------------------------------------


/* GET home page. */
router.get('/', function (req, res, next) {
  res.render('index');
});

router.get('/result', function (req, res, next) {
  res.render('result', { pythonScriptOutput: '' });
});


router.post('/result', async function (req, res, next) {
  const url = req.body.url;
  // const scriptPath = 'C://Users/Manav Rathod/Desktop/youtubeV3/main.py';
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

    const { positive_table,
      neutral_table,
      negative_table,
      countTotal,
      countPositive,
      countNeutral,
      countNegative,
      positive_list,
      neutral_list,
      negative_list, allComments } = pythonData;

      console.log("Python script executed successfully, output variables generated")

    // const topicsPrompt = `Extract exactly 15 future video topics from the following YouTube comments and present them in numbered points. These are the YouTube comments:\n${allComments.join('\n')}\n\n. Make sure that the response directly starts with the points without any extra starting or ending message`;
    // const critisismPrompt = `Extract criticism or need of improvement from the following YouTube comments and present them in numbered points. These are the YouTube comments:\n${allComments.join('\n')}\n\n. Make sure that the response directly starts with the points without any extra starting or ending message`;
    // const qnaPrompt = `Extract only repeated questions from the following YouTube comments and present them in numbered points. These are the YouTube comments:\n${allComments.join('\n')}\n\n. format the questions in single sentence and to the point. Make sure that the response directly starts with the points without any extra starting or ending message`;


    const topicsPrompt = `Extract 10 - 15 future video topics from the following YouTube comments and present them in numbered points. These are the YouTube comments:\n${allComments.join('\n')}\n\n. keep all the points short and simple and all the topics ypu suggest should be what viewers are demanding in the given comments `;
    const critisismPrompt = `Extract criticism from the following YouTube comments and present them in numbered points. These are the YouTube comments:\n${allComments.join('\n')}\n\n. Make sure that the response directly starts with the points without any extra starting or ending message`;
    const qnaPrompt = `Extract only repeated questions from the following YouTube comments and present them in numbered points. These are the YouTube comments:\n${allComments.join('\n')}\n\n. format the questions in single sentence and to the point. Make sure that the response directly starts with the points without any extra starting or ending message`;

    const prompts = [
      { role: "user", content: topicsPrompt },
      { role: "user", content: critisismPrompt },
      { role: "user", content: qnaPrompt },
    ];

    const responses = await Promise.all(
      prompts.map((prompt) => GPT.chatCompletion([prompt]))
    );

    const topics_response = responses[0];
    const critisism_response = responses[1];
    const qna_response = responses[2];

    
    let topics = topics_response;
    let critisism = critisism_response;
    let qna = qna_response;
    
    if(topics != null && critisism != null && qna != null){
      topics = topics.replace(/\\n/g, '<br>').replace(/\*/g, '-');
      critisism = critisism.replace(/\\n/g, '<br>').replace(/\*/g, '-');
      qna = qna.replace(/\\n/g, '<br>').replace(/\*/g, '-');
    }

    
    console.log(topics,critisism,qna)
    
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
      topics,
      critisism,
      qna
    });

  } catch (error) {
    console.error('Error:', error);
    // Handle error rendering here
    res.status(500).send("Internal Server Error");
  }
});




module.exports = router;
