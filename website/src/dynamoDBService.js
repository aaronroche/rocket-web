import AWS from 'aws-sdk';

AWS.config.update({ region: 'us-east-1' });

const dynamodb = new AWS.DynamoDB.DocumentClient();

export async function getDataFromDynamoDB() {
  const params = {
    TableName: 'ttest',
  };

  try {
    const data = await dynamodb.scan(params).promise();
    return data.Items;
  } catch (error) {
    console.error('Error fetching data from DynamoDB:', error);
    throw error;
  }
}

