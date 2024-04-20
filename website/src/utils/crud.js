const AWS = require('aws-sdk');

AWS.config.update({region:'us-east-1'});

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