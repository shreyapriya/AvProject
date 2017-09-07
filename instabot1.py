import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


ACCESS_TOKEN = "1590053265.ea1881f.532e178aaf324d92a129ddd68543b2a8"
#Sandbox Users : AVinstaBot.test0, AVinstaBot.test1, AVinstaBot.test2....... AVinstaBot.test10

BASE_URL = "https://api.instagram.com/v1/"


def get_data_from_url(url):
    r = requests.get(url)
    return r.json()['data']

# function for getting our own information :
def self_info():
    url = BASE_URL + "users/self/?access_token=%s"%ACCESS_TOKEN
    print "GET request url : %s"%url
    r = requests.get(url).json()

    if r['meta']['code'] == 200:
        #return r['data']
        if len(r['data']):
            print 'Username:%s'%(r['data']['username'])
            print 'No. of followers: %s'%(r['data']['counts']['followed_by'])
            print 'No. of people you are following: %s'%(r['data']['counts']['follows'])
            print 'No. of posts: %s'%(r['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        return "you have entered wrong details. Status code other than 200 received!"

# function to get user id:
def get_user_id(instagram_username):
    '''
        code
    '''
    url = BASE_URL + "users/search?q=%s&access_token=%s"%(instagram_username,ACCESS_TOKEN)
    print "GET request url : %s"%url
    #users = requests.get(url).json()['data'] [0] ['id']
    users = requests.get(url).json()
    #return users
    if users['meta']['code'] == 200:
        if len(users['data']):
            return users['data'][0]['id']
            # print user_info['data']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()

#get information of the user:
def get_user_info(user_id):
    '''
       1. make the url
       2. make the request
    '''
    user_id = get_user_id(instagram_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    url = BASE_URL + "users/%s?access_token=%s"%(user_id,ACCESS_TOKEN)
    # https: // api.instagram.com / v1 /cc users / {user - id} /?access_token = ACCESS - TOKEN
    print "GET request url : %s"%url
    r = requests.get(url).json()

    #return user_info
    if r['meta']['code'] == 200:
        if len(r['data']):
            print 'Username: %s'%(r['data']['username'])
            print 'No. of followers: %s'%(r['data']['counts']['followed_by'])
            print 'No. of people you are following: %s'%(r['data']['counts']['follows'])
            print 'No. of posts: %s'%(r['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'The profile of the user is private....so ask him/her to remove security from profile picture to see posts info:'


def download_image(url):
    '''
    download the image for the given url
    '''
    urllib.urlretrieve(item['url'],item['name'])
    return None

# Function to get your recent post:
def get_own_posts():
    '''
    get my instagram posts within range max_id and min_id
    '''

    url = BASE_URL + "users/self/media/recent?access_token=%s"%ACCESS_TOKEN
    print "GET request url : %s"%url
    r = requests.get(url).json()
    #data = r.json()['data']
    #images = [] don't uncomment this line

    #WE CAN UNCOMMENT BELOW 8 LINES USING FOR-LOOP ALSO INCASE WE DO NOT USE IF-ELSE METHOD

    #for e in data:
        #images.append({
            #'url'  :   e['images']['standard_resolution']['url'],
            #'name'  :   e['id'] + ".jpg"
        #})
    #for e in images:
        #download_image(e)
    #return images
    if r['meta']['code'] == 200:
        if len(r['data']):
            image_name = r['data'][0]['id'] + '.jpg'
            image_url = r['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

# Function to get recent post of the user:
def get_user_posts(instagram_username):
    '''
    1. search the user and get id
    2. get the recent post of the user
    '''

    user_id = get_user_id(instagram_username)
    if user_id == None:
        print 'User does not exist!'
    exit()
    url = BASE_URL + "users/%s/media/recent?access_token=%s"%(user_id , ACCESS_TOKEN)
    print "GET request url : %s"%request_url
    #data = get_data_from_url(url)
    #return data
    r = requests.get(url).json()
    if r['meta']['code'] == 200:
        if len(r['data']):
            image_name = r['data'][0]['id'] + '.jpg'
            image_url = r['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

#post id of the recent post:
def get_post_id(instagram_username):
    user_id = get_user_id(instagram_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    url = (BASE_URL + 'users/%s/media/recent/?access_token=%s')%(user_id, ACCESS_TOKEN)
    print "GET request url : %s"%url
    r = requests.get(url).json()

    if r['meta']['code'] == 200:
        if len(r['data']):
            return r['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()

# Function to like a post of the user:
def like_a_post(username):
    posts_data = get_user_posts(username)
    posts_data = posts_data[0]
    url = BASE_URL + "media/%s/likes"%(posts_data['id'])
    params = {
        "access_token" : ACCESS_TOKEN
    }
    print "POST request url :%s"%url
    r = requests.post(url , params).json()
    #return r
    if r['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


    #posts_data = get_post_id(insta_username)
    #url = (BASE_URL + 'media/%s/likes') % (media_id)


# Function to comment on users post:
def comment_on_post(post_id):
    url = BASE_URL + "media/%s/comments"%post_id
    print 'POST request url : %s' %url
    params = {
        "access_token" : ACCESS_TOKEN,
        "text" : "Testing using Instabot",
        "comment_text" : raw_input("Your comment: ")
    }
    r = requests.post(url, params).json()
    #return r
    if r['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


def get_post_comments(post_id):
    url = BASE_URL + "media/%s/comments?access_token=%s"%(post_id, ACCESS_TOKEN)
    data = get_data_from_url(url)
    return data

def get_comment_sentiment(text):
    blob = TextBlob(text, analyzer = NaiveBayesAnalyzer())
    return blob.sentiment

def delete_negative_comment(insta_username):
    '''
     1. get most recent post
     2. fetch comments on post
     3. find out negative comments
     4. delete the negative comments

     :return:
    '''
    #most_recent_post = get_user_posts(insta_username)[0]
    #comments_on_post = get_post_comments(most_recent_post["id"])

    #check if a comment is negative
   # most_recent_comment = comments_on_post[0]
    #blob = TextBlob(most_recent_comment["text"], analyzer = NaiveBayesAnalyzer())
    #return blob

#or use it


    media_id = get_post_id(insta_username)
    url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s'%url
    r = requests.get(url).json()

    if r['meta']['code'] == 200:
        if len(r['data']):
            for x in range(0, len(r['data'])):
                comment_id = r['data'][x]['id']
                comment_text = r['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'

#a = comment_on_post("1576387517484312928_1590053265")
#print a.content

#a = like_a_post("avantika.i.n.f.i.n.i.t.e")
#dir(a)
#print get_comment_sentiment("get lost")
#print get_comment_sentiment("good bad")
#print get_comment_sentiment("you are great")
#print get_comment_sentiment("you are beautiful")
#print get_comment_sentiment("you are looking ugly")



def start_bot():
    while True:
        print '\n'
        print 'congratulations!  your instabot has started'
        print 'your menu options are:'
        print "1.Get your own details\n"
        print "2.Get your user id\n"
        print "3.Get your details of a user by username\n"
        print "4.Get your own recent post\n"
        print "5.Get the recent post of a user by username\n"
        print "6.Get the recent post's post id\n"
        print "7.Like the recent post of a user\n"
        print "8.comment on the recent post of the user\n"
        print "9.get the sentiment of the comment\n"
        print "10.Delete a negative comment\n"
        print "11.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "1":
            self_info()
        elif choice == "2":
            insta_username = raw_input("Enter the username of the user: ")
            print get_user_id(insta_username)

        elif choice == "3":
            insta_username = raw_input("Enter the username")
            get_user_info(get_post_id(insta_username))

        elif choice == "4":
            get_own_posts()
        elif choice == "5":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_posts(insta_username)
        elif choice == "6":
            insta_username = raw_input("Enter the username of the user: ")
            get_post_id(insta_username)
        elif choice=="7":
            like_a_post(username)
        elif choice=="8":
            comment_on_post(post_id)
        elif choice == "9":
            get_comment_sentiment()
            print get_comment_sentiment("get lost")
            print get_comment_sentiment("good bad")
            print get_comment_sentiment("you are great")
            print get_comment_sentiment("you are beautiful")
            print get_comment_sentiment("you are looking ugly")
        elif choice=="10":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
        elif choice == "11":
            exit()
        else:
            print "wrong choice"
start_bot()