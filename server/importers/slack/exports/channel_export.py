import os, csv, time, datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def export_channel_history(token, channel_id, output_file="slack_export.csv"):
    """
    Export all messages and their timestamps from a Slack channel using a user token.
    
    Args:
        token (str): Slack User OAuth Token starting with xoxp-
        channel_id (str): The ID of the channel to export (starts with C)
        output_file (str): Name of the output CSV file
    """
    # Create exports directory if it doesn't exist
    exports_dir = os.path.join(os.getcwd(), "exports")
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
        print(f"Created directory: {exports_dir}")
    
    # Set full path for the output file
    full_output_path = os.path.join(exports_dir, output_file)

    client = WebClient(token=token)

    try:
        response = client.conversations_info(channel=channel_id)
        channel_name = response["channel"]["name"]
        print(f"Exporting channel: #{channel_name}")
    except SlackApiError as e:
        print(f"Error checking channel: {e.response['error']}")
        print("Make sure you have access to this channel and the token has the right permissions")
        return
    
    #open csv for writing
    with open(full_output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['timestamp', 'date', 'message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        #initialize variables for pagination
        cursor = None
        more_messages = True
        message_count = 0

        print("Starting export ...")

        #loop until all messages are retrieved
        while more_messages:
            try:
                if cursor:
                    result = client.conversations_history(
                        channel=channel_id,
                        cursor=cursor,
                        limit=1000
                    )
                else:
                    result = client.conversations_history(
                        channel=channel_id,
                        limit=1000
                    )
                
                #process messages
                messages = result['messages']

                for msg in messages:
                    ts = float(msg.get("ts", 0))
                    date_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                    #extract message
                    message_text = msg.get("text", "")  

                    #write to CSV
                    writer.writerow({
                        'timestamp': ts,
                        'date': date_str,
                        'message': message_text
                    })
                    
                    message_count += 1
                
                more_messages = result["has_more"]
                if more_messages:
                    cursor = result["response_metadata"]["next_cursor"]
                    time.sleep(1.2)
                    print(f"Retrieved {message_count} messages so far...")
            
            except SlackApiError as e:
                print(f"Error retrieving messages: {e.response['error']}")
                if e.response['error'] == "ratelimited":
                    delay = int(e.response.headers.get("Retry-After", 60))
                    print(f"Rate limited. Retrying after {delay} seconds...")
                    time.sleep(delay)
                    continue
                else:
                    break
    print(f"Export complete! {message_count} messages exported to {full_output_path}")

if __name__ == "__main__": 
    # Get the Slack token and channel ID from environment variables or user input
    token = os.environ.get("SLACK_USER_TOKEN")
    channel_id = os.environ.get("SLACK_CHANNEL_ID")
    
    if not token:
        token = input("Enter your Slack User OAuth Token (xoxp-...): ")
    
    if not channel_id:
        channel_id = input("Enter the Channel ID (C...): ")
    
    output_file = input("Enter output filename (default: slack_export.csv): ") or "slack_export.csv"
    
    export_channel_history(token, channel_id, output_file)


