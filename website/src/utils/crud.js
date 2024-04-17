const AWS = require('aws-sdk');


AWS.config.update({
  region: 'us-east-1',
  accessKeyId: process.env.REACT_APP_AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.REACT_APP_AWS_SECRET_ACCESS_KEY
});


const docClient = new AWS.DynamoDB.DocumentClient();


const getAllItems = async (tableName) => {
    const params = {
      TableName: tableName
    };
    return docClient.scan(params).promise();
};


// getAllItems('rocket-web')
//   .then(data => console.log(data))
//   .catch(error => console.error(error));

module.exports = { getAllItems };