Title: Directly uploading a Pandas DataFrame to S3
Date: 2018-10-30 15:30
Modified: 2018-10-30 15:30
Category: S3
Tags: python, pandas, s3, code snippet
Slug: direct_upload_to_s3
Authors: Sam Zuckerman
Summary: Here's some basic code on how to upload to S3 directly from a Pandas object.


Recently I published a post on [easily uploading data to S3 and loading into Redshift]({filename}/get_data_into_redshift.md). That post was mainly focused on saving the data as a local file and uploading to S3 using either boto3 or the AWS CLI to move the file to S3.

However, even though the above works, I had a situation recently where I wanted to upload the files to S3 without storing any temporary files locally.

I saw a [great stackoverflow answer](https://stackoverflow.com/a/40615630) that discusses how to use boto3 to upload the bytes from a DataFrame to S3.

Here's the answer from the post:

```python
from io import StringIO
import boto3
 
csv_buffer = StringIO()
df.to_csv(csv_buffer)
s3_resource = boto3.resource('s3')
s3_resource.Object(bucket, 'df.csv').put(Body=csv_buffer.getvalue())
```

The main point to realize here is that instead of the file being sent as a 'file' it's getting sent as bytes directly over the internet.

This is a good, quick solution, however, if you have a super-gigantic file, it might still be better to go the 'temporary file' route, since this has to store the object in memory to send it.

The main idea that's important about this method, though, is that once you're familiar with using the methods from the [`io` package](https://docs.python.org/3/library/io.html) (i.e. `StringIO()` and `BytesIO()`), there's a ton you can do online.

For example, using `BytesIO()` you can download and work with images using `PIL`, using `StreamIO()` you can work with huge text files that won't fit in memory; there's many cool uses that will take your Python programming to the next level. 

But those are the topics for other posts :). This is merely an introduction to one example using the `io` module.

  