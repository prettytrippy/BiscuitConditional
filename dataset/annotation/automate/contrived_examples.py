import numpy as np

contrived_examples = [
    ("I knew that if these were the guys I was looking for, I'd have to set up a deal so sweet, they wouldn't be able to walk away from it.", "0"),
    ("Jacob, if it was any other brain but yours, I might agree", "0"),
    ("It says: \"America stands for freedom, but if you think you're free...\"", "0"),
    ("The Sporting News should know about it.. 247 home runs in the minors would be a dubious honor, if ya think about it.", "1"),
    ("I wouldn't keep coming here if I didn't like you.", "0"),
    ("What if he caps me before you can make a move?", "0"),
    ("Listen, Maude, I'm sorry if your stepmother is a nympho, but I don't see what it has to do with--do you have any kalhua?", "0"),
    ("Sometimes, if a girl retires, she'll even sell it worth good money", "0"),
    ("But if he makes you happy, you go right ahead", "0"),
    ("Sir, I came from the Chicago offices myself, and if I may say, sir, there are still some very good....", "1"),
    ("I grant you your wish if you grant Lady Guenevere hers.", "0"),
    ("Look, if you really wanna score some dope, I got the guy.", "0"),
    ("Sir, if the subs haven't left by now...", "0"),
    ("I was wondering if it's better to ask your girlfriend for the money", "0"),
    ("So if they didn't ask for you to be here, how did you know to come?", "0"),
    ("What kind of work do you do, Barton, if you don't mind my asking?", "0"),
]

np.random.shuffle(contrived_examples)