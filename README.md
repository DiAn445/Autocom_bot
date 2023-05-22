### Autocom_bot
<b>You need to use this command to install all dependencies and then run bot:</b>
<pre>pip install -r requirements.txt</pre>

<b>First of all add the bot to the group where you are admin</b>

<b>Then use those commands to continue:</b>
<pre> /moderator <b> to go through "if admin" checking (admin keyboard will appear in bot_chat)</b></pre>
<pre> /delete <b> to delete messages from DB </b></pre>
### Working with chat bot keyboard
<pre> /upload <b> this command in bot_chat will start the machine state, so you will be able to add messages to DB </b></pre>
<pre> /cancel <b> to finish the machine state </b></pre>
<pre> /messagelist <b> to watch all saved messages from DB and choose one to start sending</b></pre>
<pre> /random <b> to start sending random messages from DB </b></pre>

### Buttons are not gonna work without going through "if admin" checking 

### About the autocommenting:
    It makes 4 rounds during the day, 8400 comments in common;
    Random sending time;
    Using free proxy from proxy_list (Needed to be filled up with new ones from https://advanced.name/ru/freeproxy to work out properly);
    Changing proxy every 5 comments to the next one from proxy list;