"""All the words on sheishome.co.uk, transcribed from the approved mockups in
SHE_Website_Page_Map_Canva_Ready_FIXED. Edit here; run build.py; the site updates.
Images are the crops made by tools/crop_assets.py (names without .webp)."""
from __future__ import annotations

CHAPTERS = [
    {"slug": "becoming", "close": "becoming-4", "name": "Becoming", "tag": "Discover what's possible", "tile": "tile-becoming", "card": "tile-becoming",
     "sub": "A deeper you is already here.", "intro": "It's time to listen, get curious and reconnect with what really matters to you.",
     "sections": [
         {"k": "What do I actually want?", "paras": ["In the busyness of everyday life, it's easy to lose touch with yourself. This is a space to pause, get honest and start asking deeper questions.", "Because change often begins with awareness."], "img": "becoming-1"},
         {"k": "Give yourself the space to explore.", "paras": ["You don't need to have all the answers. You just need to be open to the questions.", "This is about reconnecting with yourself, your values and what truly matters to you."], "img": "becoming-3"},
         {"k": "A more aligned you", "paras": ["The more you understand yourself, the easier it becomes to make choices that feel right.", "This is the beginning of a deeper, more intentional life."], "img": "becoming-4"},
     ],
     "here_img": "becoming-2",
     "here": ["you feel like something is missing", "you're going through a period of change", "you're questioning what you want", "you're ready to understand yourself better", "you're craving more meaning, alignment or fulfilment", "you want to feel more like you again"],
     "ways": {"explore": "Stories, conversations and ideas about self-discovery and intentional living.", "gather": "Experiences that help you connect, reflect and feel more like you.", "tools": "Practical resources to help you go deeper and get clearer on what you want."},
     "closing": "It starts with you."},
    {"slug": "resetting", "close": "resetting-4", "name": "Resetting", "tag": "Create space and clarity", "tile": "tile-resetting", "card": "tile-resetting",
     "sub": "Sometimes you need space to move forward.", "intro": "Step away, slow down and give yourself the time and space you need.",
     "sections": [
         {"k": "It's okay to pause.", "paras": ["You don't have to keep pushing.", "Sometimes the most productive thing you can do is stop.", "Stepping away can help you see things more clearly, reduce overwhelm and create the space you need for what's next."], "img": "resetting-1"},
         {"k": "A calmer, clearer you", "paras": ["When you give yourself space, you create room to breathe, reflect and make decisions that feel right for you.", "Resetting isn't about doing less. It's about making space for what matters."], "img": "resetting-3"},
         {"k": "From overwhelm to perspective", "paras": ["A different pace can help you see things more clearly.", "It can give you the perspective you need to move forward with more intention, more energy and a renewed sense of what you want."], "img": "resetting-4"},
     ],
     "here_img": "resetting-2",
     "here": ["you feel overwhelmed or burnt out", "you need a break from your usual routine", "you're feeling stuck or unsure", "you're craving more space, time or clarity", "you know something needs to change", "you're ready to slow down and reset"],
     "ways": {"explore": "Stories, conversations and ideas about slowing down, clarity and simpler living.", "gather": "Experiences that give you space to reflect, reset and reconnect.", "tools": "Practical resources to help you manage overwhelm and create more balance."},
     "closing": "Sometimes a break is the beginning."},
    {"slug": "blooming", "close": "blooming-4", "name": "Blooming", "tag": "Feel your life open up", "tile": "tile-blooming", "card": "tile-blooming",
     "sub": "You're not too much, you're becoming more you.", "intro": "A space to embrace who you are, celebrate your growth and let more of you into your life.",
     "sections": [
         {"k": "It's time to let more of you in.", "paras": ["You've done the inner work. You've created space. Now it's time to embrace your growth and explore what's possible.", "This is about confidence, self-expression and living more fully."], "img": "blooming-1"},
         {"k": "Grow at your own pace.", "paras": ["Blooming isn't about being perfect. It's about giving yourself permission to grow, explore and become more of who you are, in your own time, in your own way."], "img": "blooming-3"},
         {"k": "A brighter, more open you", "paras": ["When you allow yourself to bloom, new opportunities, connections and possibilities naturally start to appear.", "You don't have to do it all. You just have to keep showing up."], "img": "blooming-4"},
     ],
     "here_img": "blooming-2",
     "here": ["you're starting to feel more like yourself", "you're ready to embrace change", "you want to build more confidence", "you're excited about what's next", "you're ready to say yes to more", "you want to live a life that feels good (and true to you)"],
     "ways": {"explore": "Stories, conversations and ideas about confidence, self-expression and living more fully.", "gather": "Experiences that bring women together to celebrate growth and new possibilities.", "tools": "Practical resources to help you build confidence and take the next step."},
     "closing": "More you. That's a beautiful thing."},
    {"slug": "rising", "close": "rising-1", "name": "Rising", "tag": "Speak, act, take up space", "tile": "tile-rising", "card": "tile-rising",
     "sub": "You're ready to take up more space.", "intro": "You've found something you want. Now you're ready to trust yourself enough to go after it.",
     "sections": [
         {"k": "Maybe you're ready for more.", "paras": ["More responsibility.\nMore freedom.\nMore honesty.\nMore creativity.\nMore space.\nMore of the things you've been telling yourself you'll do \"one day.\"", "You know what you want. Or perhaps you have a pretty good idea.", "Now the question is whether you believe in yourself enough to actually go for it."], "img": "rising-1"},
         {"k": "Say it.", "h": "Sometimes rising starts with your voice.", "paras": ["Saying what you mean.\nAsking for what you want.\nSaying no when you mean no.\nSaying yes when you mean yes.\nLetting yourself be heard."], "img": "rising-3"},
         {"k": "What if you actually believed you could?", "paras": ["Not because you know exactly how it's going to work.\nNot because you're guaranteed to succeed.\nBecause you trust yourself enough to try.", "You don't need everyone else to believe in you first.\nYou need to believe in you.", "You get to decide what happens next."], "img": "rising-4"},
         {"k": "So what are you going to do?", "h": "Sometimes the biggest shift is deciding you're no longer going to wait.", "paras": ["Take the opportunity.\nHave the conversation.\nMake the decision.\nPut yourself forward.\nStart the thing.", "You don't have to know exactly how it will unfold.\nYou just have to take the first step."], "img": "", "wide": True},
     ],
     "here_img": "rising-2",
     "here": ["you've been playing it safe for longer than you'd like", "there's something you've wanted to do for ages", "you're ready to speak up about what you really want", "you're tired of waiting for someone else to give you permission", "you're ready to take a risk", "you know you're capable of more", "you're ready to trust yourself"],
     "ways": {"explore": "Stories, conversations and ideas about confidence, self-belief, voice and stepping into more.", "gather": "Experiences that bring women together to connect, challenge themselves and take up space.", "tools": "Practical resources to help you move from thinking about it to doing something about it."},
     "closing": "You don't need permission.\nYou just need to decide."},
    {"slug": "letting-go", "close": "letting-go-5", "name": "Letting Go", "tag": "Release what no longer belongs", "tile": "tile-letting-go", "card": "tile-letting-go",
     "sub": "Something is ending, and you're learning how to let it go.", "intro": "You don't have to keep carrying what no longer belongs to you. There's freedom in release.",
     "sections": [
         {"k": "What are you still carrying?", "paras": ["Sometimes you know something has run its course.", "Sometimes it's a person. A relationship. A job. A habit. A fear. A belief. An expectation.", "Sometimes you can't quite explain why you're still holding onto it.", "You just know it's taking up space that you want for something else."], "img": "letting-go-1"},
         {"k": "You don't have to carry it with you.", "paras": ["Letting go doesn't mean it didn't matter. It means you accept what it was, and choose what happens next.", "Some things need to be understood.\nSome things need to be felt.\nSome things simply need to be released."], "img": "letting-go-3"},
         {"k": "What are you ready to put down?", "paras": ["You get to decide what comes with you.", "You don't have to keep a person, a pattern, a fear or an old story simply because it's been part of your life.", "Sometimes freedom begins with deciding that something has had enough of your energy."], "img": "letting-go-4"},
         {"k": "Make room.", "paras": ["When you stop carrying what no longer belongs to you, there's room for something else.", "More energy.\nMore choice.\nMore freedom.", "And eventually, a new page."], "img": "letting-go-5"},
     ],
     "here_img": "letting-go-2",
     "here": ["something from your past still has a hold on you", "you're repeating a habit you know you want to leave behind", "you're carrying someone else's expectations", "you've outgrown a relationship, role or version of yourself", "you're ready to stop giving your energy to something that no longer belongs in your life", "you keep saying \"I know I need to let this go\""],
     "ways": {"explore": "Stories, conversations and ideas about endings, change, release and moving forward.", "gather": "Experiences that give you space to reflect, release and reconnect.", "tools": "Practical resources to help you explore what you're ready to leave behind."},
     "closing": "You don't have to take everything with you."},
    {"slug": "beginning-again", "close": "beginning-again-4", "name": "Beginning Again", "tag": "A fresh page, on your terms", "tile": "tile-beginning-again", "card": "tile-beginning-again",
     "sub": "You're starting again, perhaps differently this time.", "intro": "A fresh page. A new chapter. The freedom to create a life that feels like you.",
     "sections": [
         {"k": "There's nothing wrong with starting again.", "paras": ["Maybe something ended.\nMaybe something changed.\nMaybe you simply decided that the life you were living wasn't the life you wanted anymore.", "Starting again doesn't mean starting from scratch.\nYou bring everything you've learned with you."], "img": "beginning-again-1"},
         {"k": "You get to choose what comes with you.", "paras": ["You don't have to erase who you've been.", "Keep what you love.\nKeep what you've learned.\nKeep the parts of yourself that feel true.", "Leave the rest behind.\nAnd begin from there."], "img": "beginning-again-3"},
         {"k": "Imagine having no idea what happens next, and being completely okay with that.", "paras": ["There is something freeing about a beginning.", "You don't have to know exactly how it will unfold.\nYou get to explore.\nTry something.\nChange your mind.\nPaint another layer.\nSee what happens."], "img": "beginning-again-4"},
         {"k": "This is your page.", "paras": ["You already have the picture in your mind.", "Now you get to start creating it."], "img": "beginning-again-5"},
     ],
     "here_img": "beginning-again-2",
     "here": ["you're standing at the beginning of something unfamiliar", "you've made a decision that changes what's next", "you're creating a new life after an ending", "you've realised you want to do things differently this time", "you're excited about what's ahead, even if you don't have it all figured out", "you're ready to see what happens when you give yourself permission to begin"],
     "ways": {"explore": "Stories, conversations and ideas for new starts and new directions.", "gather": "Experiences for women stepping into something new.", "tools": "Practical resources to help you turn possibility into something real."},
     "closing": "You don't have to know exactly how it will unfold.\nYou just have to begin."},
]

CONVERSATIONS = [
    # Emily's own story. Her words and her photographs come from the page she designed
    # ("is this it?" in her pictures folder). It stops where her draft stops, at the phone call.
    {"slug": "is-this-it", "cat": "Founder conversation", "title": "Is This It?", "read": "10 min read",
     "img": "conv-isthisit", "chapter": "becoming", "has_page": True,
     "side": "isthisit-side", "main": "isthisit-main", "band": "isthisit-band"},
    {"slug": "i-left-my-career-at-42", "cat": "Career", "title": "I left my career at 42, and found myself again.", "read": "12 min read", "img": "conv-1", "chapter": "becoming", "has_page": True},
    {"slug": "until-i-became-a-mother", "cat": "Motherhood", "title": "I didn't realise how lost I felt until I became a mother.", "read": "10 min read", "img": "conv-2", "chapter": "resetting"},
    {"slug": "starting-again-at-50", "cat": "Identity", "title": "Starting again at 50, and finally choosing myself.", "read": "14 min read", "img": "conv-3", "chapter": "beginning-again"},
]
QUESTIONS = [
    {"slug": "five-years", "title": "Where do you think you'll be in five years if you keep going the way you are now?", "read": "4 min read", "img": "q-1", "chapter": "becoming"},
    {"slug": "couldnt-fail", "title": "What would you do if you knew you couldn't fail?", "read": "3 min read", "img": "q-2", "chapter": "rising"},
    {"slug": "living-or-managing", "title": "Are you living your life, or just managing it?", "read": "5 min read", "img": "q-3", "chapter": "resetting"},
]
# What a SHE gathering can be. Retreats have their own page, so they are not repeated here.
EXPERIENCES = [
    {"name": "Workshops", "sub": "Practical tools for a more intentional life.", "img": "exp-workshops", "href": "/gather/create-your-next-chapter/"},
    {"name": "Walks", "sub": "Time in nature, with conversation that goes deeper.", "img": "exp-walks", "href": "/gather/experiences/"},
    {"name": "Coffee mornings", "sub": "Casual meet-ups, real conversations.", "img": "exp-coffee", "href": "/gather/experiences/"},
    {"name": "Suppers", "sub": "A long table, good food and honest talk.", "img": "exp-suppers", "href": "/gather/experiences/"},
]
EVENTS = [
    {"date": "Date to be announced", "place": "Warwick", "name": "Create Your Next Chapter",
     "sub": "A half-morning workshop with practical tools and meaningful conversation.",
     "img": "way-workshops", "href": "/gather/create-your-next-chapter/"},
    # Nothing is booking yet. These say so plainly rather than pretending there is a date.
    {"date": "Coming soon", "place": "", "name": "Coffee Mornings",
     "sub": "No coffee mornings just now. Keep an eye out: the next one is coming soon.",
     "img": "way-coffee", "href": "", "soon": True},
    {"date": "Coming soon", "place": "", "name": "SHE Retreats",
     "sub": "No retreats are booking just now. Join SHE and you will hear first.",
     "img": "way-retreats", "href": "", "soon": True},
]


def page(path, template, title, description="", image="", orb=False, **data):
    return {"path": path, "template": template, "title": title, "description": description, "image": image, "orb": orb, "data": data}


# The Scottish Hills retreat and the London Coffee Morning are not running at the moment
# (founder's decision, 21 September 2026). Their pages were removed from the site rather than
# left live with old dates; the Gather page says both are coming soon. Their words are in git
# history at commit 9286c89 if they are wanted again.

def pages() -> list[dict]:
    out = [
        page("/", "home.html", "SHE is home. For every chapter of becoming", "A space to feel, explore, and come back to yourself. Find your chapter, gather in real life, explore conversations and journals.", "home-hero", orb=True, chapters=CHAPTERS),
        page("/about/", "about.html", "About SHE", "What started with a journal became an experience. Where SHE came from, and why it is about both becoming and belonging.", "about-hero"),
        page("/gather/create-your-next-chapter/", "event.html", "Create Your Next Chapter, a SHE workshop", "A half-morning workshop to help you pause, reflect and intentionally shape what's next.", "cync-hero",
             ev={"kicker": "Workshop", "title": "Create Your\nNext Chapter", "tags": "Vision boarding · Manifestation · Mindset", "tags2": "Coffee. Cake. Clarity. You.",
                 "intro": "A half-morning workshop to help you pause, reflect and intentionally shape what's next, with practical tools, meaningful conversation and a supportive community of women.",
                 "hero": "cync-hero", "about_img": "cync-about", "expect_img": "cync-expect", "bottom": "cync-bottom", "cta": "Join SHE for the date",
                 "when": "More details to be released soon", "time": "", "where": "Warwick", "where_sub": "", "group": "A small, intimate group", "extra": "Coffee, tea and cake included", "price": "",
                 "about_title": "About this event", "about": ["Life moves in seasons, and sometimes we find ourselves at a turning point, not knowing exactly what's next, but feeling ready for something different.", "This workshop is an invitation to step out of the everyday, create space for yourself and explore your next chapter with intention. Through vision boarding, reflection, mindset work and meaningful conversation, you'll leave feeling clearer, more grounded and inspired about what's ahead.", "Whether you're navigating a big change or simply want to realign, this is a morning to invest in you."],
                 "expect": [("Vision boarding", "Get clear on what you want and bring your next chapter to life."), ("Mindset", "Explore what's possible and shift the beliefs that may be holding you back."), ("Meaningful conversation", "Share, listen and be inspired by like-minded women."), ("Practical tools", "Leave with clarity, intention and simple next steps.")],
                 "who": ["Women at any stage of life", "Those feeling ready for change", "Anyone who wants more clarity and direction", "Women who value honest conversation and real connection"],
                 "closing": "A morning for\na brighter you."}),
        page("/gather/retreats/", "retreats.html", "SHE Retreats", "Different places. Different experiences. Something to explore. SHE retreats are created for women who want to step away from everyday life.", "retreats-hero",
             intro=["SHE retreats are created for women who want to step away from everyday life and experience something a little different. Beautiful places. Interesting women. Space to breathe, think and reconnect. Experiences that invite you to explore what matters to you.", "And no two retreats are the same."],
             what=["Every SHE retreat is different, but they all share the same intention, to create space for something to shift. Whether it's a weekend close to home or a longer journey further afield, each retreat offers a considered combination of beauty, experience, and connection."],
             pillars=[("home", "A beautiful place", "Chosen intentionally for the experience."), ("leaf", "Something to explore", "A theme, a practice or a new perspective."), ("sun", "A SHE experience", "Thoughtfully curated and unique to each retreat."), ("people", "Real connection", "Genuine conversations and a supportive community of women."), ("heart", "Your SHE journal", "A lasting record of your experience to take home.")],
             journal="Every woman receives a SHE journal as part of the retreat experience. Choose your colour before you arrive, and make it yours, a place for thoughts, reflections, creativity and memories.",
             current=None, was_current={"name": "The Scottish Hills", "theme": "Sound · Stillness · Connection", "dates": "17 to 21 April 2026", "place": "Scottish Highlands, UK", "group": "A small group experience", "img": "scottish-about", "href": "/gather/retreats/the-scottish-hills/"}),
        page("/join/", "join.html", "Join SHE", "Come in. Stay a while. Join the SHE Letter and the community.", "join-hero", orb=True),
        page("/chapters/", "chapters.html", "The Chapters", "Wherever you are, you belong here. Six chapters. Find the one that feels most like you.", "chapters-hero", chapters=CHAPTERS),
    ]
    for c in CHAPTERS:
        out.append(page(f"/chapters/{c['slug']}/", "chapter.html", f"{c['name']}, a chapter of SHE", c["sub"], f"{c['slug']}-hero", c=c, chapters=CHAPTERS))
    out += [
        page("/explore/", "explore.html", "Explore", "Real conversations. Bigger questions. Stories, conversations and questions to make you pause, think and see something differently.", "explore-hero", conversations=CONVERSATIONS, questions=QUESTIONS),
        page("/explore/conversations/i-left-my-career-at-42/", "story.html", "I left my career at 42, and found myself again", "For years I thought I was living the dream. A good job, a steady income, a life that looked successful on paper. But underneath, I was exhausted, resentful and completely disconnected from myself.", "story-main",
             story=CONVERSATIONS[1], meta="A woman in her forties", chapter=CHAPTERS[0], questions=QUESTIONS, conversations=CONVERSATIONS,
             standfirst="For years I thought I was living the dream. A good job, a steady income, a life that looked successful on paper. But underneath, I was exhausted, resentful and completely disconnected from myself.",
             body=[
                 {"p": ["I used to be the kind of person who said yes to everything. The promotion. The longer hours. The extra responsibility. I thought that's what you were supposed to do, right? Work hard, keep progressing, be grateful.", "And for a long time, I was.", "But somewhere along the way, I stopped checking in with myself. I was so busy building a life that looked good from the outside, that I didn't notice I was slowly disappearing on the inside."]},
                 {"h": "It all came to a head one Sunday night.", "p": ["I remember sitting on the sofa, scrolling through my emails, feeling this wave of dread for the week ahead. And I just thought, I can't do this anymore. It wasn't one dramatic event, it was the realisation that I had been feeling unhappy for so long, I had almost forgotten what happy felt like."], "img": "story-mid"},
                 {"p": ["That night, I wrote a list. Not a practical to-do list, but an honest one. What do I actually want? What makes me feel alive? What would I do if I wasn't so scared?", "It was the first time in years I had allowed myself to really ask those questions.", "The answers didn't come all at once, but that night was the beginning of everything changing."]},
             ],
             sit_with=QUESTIONS[1], familiar="You might want to explore Becoming, stories, tools and guidance for women navigating change, at any stage of life."),
        page("/explore/conversations/is-this-it/", "story.html", "Is This It?",
             "Emily, founder of SHE, on leaving England, moving to Dubai, and discovering what can happen when you change your environment.",
             "isthisit-main",
             story=CONVERSATIONS[0], meta="Emily, founder of SHE", chapter=CHAPTERS[0], questions=QUESTIONS, conversations=CONVERSATIONS,
             standfirst="Emily, founder of SHE, on leaving England, moving to Dubai, and discovering what can happen when you change your environment.",
             body=[
                 {"k": "01 / The beginning", "h": "I had a good life. So why did it feel like it wasn't enough?",
                  "p": ["I was young. I was probably a little naive. And if I'm honest, there wasn't anything particularly wrong with my life. I was living in England, I had a good job, a good salary, my Mini Cooper, and I was doing makeup, which I actually enjoyed. And I could see where my life was going. That was the strange thing. It was almost like I could see the next ten or twenty years laid out in front of me. And I remember thinking: Is this it?"],
                  "quote": "It wasn't that I was unhappy. I just felt like there had to be more.",
                  "img": "isthisit-1"},
                 {"k": "02 / The opportunity", "h": "Then the phone rang.",
                  "p": ["I remember it really clearly. I was walking down a country lane, standing by a gate and looking out across a field. I was thinking about that feeling again. Then my friend called. She had an opportunity for me. It was a sales job in Dubai. Now, this was before Dubai was the place everyone seems to know about now. I honestly didn't really know anything about the UAE. So I did what seemed like the sensible thing. I researched it. And then thought: Why not go for a couple of weeks and see? What's the worst that could happen?"],
                  "img": "isthisit-2"},
             ],
             band="Sometimes the change isn't what you think it is.",
             more_to_come="More of Emily's story is coming.",
             sit_with=QUESTIONS[1],
             familiar="You might want to explore Becoming, stories, tools and guidance for women navigating change, at any stage of life."),
        page("/explore/questions/five-years/", "question.html", "Where do you think you'll be in five years if you keep going the way you are now?", "This was the question that stopped her in her tracks. Here's what she said.", "question-hero",
             q=QUESTIONS[0], meta="Anonymous", chapter=CHAPTERS[0], questions=QUESTIONS, conversations=CONVERSATIONS,
             standfirst="This was the question that stopped her in her tracks. Here's what she said.",
             body_1=["had never really thought about it. I was just getting on with things: work, family, the constant to-do list. But when I actually sat with the question, it made me feel uncomfortable. Because the honest answer was: I'd probably be exhausted. Still saying yes to things I don't really want to do. Still putting myself last.", "I realised I've been living in this cycle of being busy, thinking that means I'm doing okay. But busy isn't the same as fulfilled. I don't want to look back in five years and realise I had the chance to make a change, and I didn't take it.", "That question gave me the clarity I needed to start making different choices. It didn't give me all the answers, but it reminded me that I do have a say in what my life looks like."],
             quote="Busy isn't the same as fulfilled.",
             body_2=["I'm still figuring things out, but I'm asking myself that question more often now. It's a simple one, but it's powerful. Because it makes me take responsibility, and it reminds me that change doesn't have to be dramatic to be meaningful."]),
        page("/gather/", "gather.html", "Gather", "Come together. In real life. From intimate coffee mornings to immersive retreats, SHE Gather brings women together in cities and spaces around the world.", "gather-hero", experiences=EXPERIENCES, events=EVENTS,
             lede="Meaningful spaces. Real conversations.\nWomen, together.", intro="From intimate coffee mornings to immersive retreats, SHE Gather brings women together in cities and spaces around the world.",
             ways_note="Our gatherings are an invitation to pause, meet like-minded women and experience something meaningful, in beautiful places, and at every stage of your journey.",
             events_intro="What is coming up, and what to keep an eye out for.",
             closing_quote="Shared spaces. Brighter chapters."),
        page("/gather/experiences/", "experiences.html", "SHE Experiences",
             "Unique gatherings. Real connections. Workshops, walks, suppers and conversations for women who want to feel more like themselves again.",
             "way-workshops", experiences=EXPERIENCES, events=EVENTS,
             intro="Thoughtfully created experiences for women to learn, share, explore and feel more like themselves again. From creative workshops to nature walks, intimate suppers to powerful conversations.",
             note="Every experience is different, but each one is small, warm and unhurried, with room to think and people worth talking to.",
             expect=[("A small group", "Never a crowd. Enough people to spark something, few enough to be heard."),
                     ("Come as you are", "No preparation, no pressure, no performance."),
                     ("Something to take home", "A tool, a question or a conversation that stays with you."),
                     ("Women who get it", "Different lives, the same honesty.")],
             events_intro="What is coming up, and what to keep an eye out for.",
             closing="Shared spaces.\nBrighter chapters."),
        page("/tools/", "tools.html", "Tools", "More than a journal. A place to pause, ask better questions, notice what's changing, imagine what's possible and come back to yourself.", "tools-hero"),
        page("/tools/the-becoming/", "becoming_journal.html", "The Becoming, a journal for a more intentional life", "A 24-week guided journal to help you look at your life, your patterns, your energy, your goals and what you want to change.", "becoming-product-hero"),
        page("/tools/shes-glowing/", "glowing_journal.html", "She's Glowing, a journal for pregnancy, motherhood and your own evolution", "You're not losing yourself. You're meeting yourself. A space to feel, reflect and stay connected to yourself through a chapter that changes everything.", "glowing-hero"),
        # Both physical journals are sold out. Nobody is sent to a shop that cannot sell them:
        # these pages say so, and take a name for when the next edition is ready.
        page("/tools/the-becoming/sold-out/", "soldout.html", "The Becoming is currently sold out",
             "The physical edition of The Becoming is sold out. Leave your details and we will let you know when it returns.",
             "becoming-product-hero",
             product="The Becoming", product_href="/tools/the-becoming/", source="The Becoming waiting list",
             sub="A journal for the chapter you're becoming.",
             hero="becoming-product-hero",
             thumbs=[{"img": "tools-becoming", "alt": "The Becoming, closed"},
                     {"img": "becoming-page", "alt": "An open page of The Becoming"},
                     {"img": "becoming-inside-1", "alt": "The check in page"},
                     {"img": "becoming-physical", "alt": "The journal held in two hands"}],
             paras=["The current physical edition of The Becoming has found its way to its last few pages, and this edition is now sold out.",
                    "We are working on the next edition, and you can be the first to know when it is ready."],
             pillars=[("book", "Thoughtfully\ndesigned"), ("leaf", "Beautiful,\nhigh quality materials"),
                      ("heart", "A companion\nthrough change"), ("sun", "Part of\nSHE Originals")],
             closer_img="becoming-page", closer_alt="An open page of The Becoming",
             closer_h="Made to return to.",
             closer="The Becoming is a journal for reflection, clarity and intentional change, made to support you through the seasons of your life with thoughtful prompts, space to write and a quiet, timeless design."),
        page("/tools/shes-glowing/sold-out/", "soldout.html", "She's Glowing is currently sold out",
             "The physical edition of She's Glowing is sold out. Leave your details and we will let you know when it returns.",
             "glowing-hero",
             product="She's Glowing", product_href="/tools/shes-glowing/", source="She's Glowing waiting list",
             sub="A journal for the beginning of motherhood.",
             hero="glowing-hero",
             thumbs=[{"img": "glowing-physical", "alt": "She's Glowing, closed"},
                     {"img": "glowing-page", "alt": "A hand writing in She's Glowing"},
                     {"img": "glowing-inside", "alt": "Two open pages of She's Glowing"},
                     {"img": "glowing-cup", "alt": "A woman holding a speckled mug"}],
             paras=["The physical edition of She's Glowing is currently sold out.",
                    "If you would like to be first to know when the next edition is available, leave your details below."],
             pillars=[("heart", "Created for\nmotherhood"), ("leaf", "Beautiful,\nhigh quality materials"),
                      ("people", "Supports your\npregnancy journey"), ("sun", "Part of\nSHE Originals")],
             closer_img="glowing-inside", closer_alt="Two open pages of She's Glowing",
             closer_h="Gentle prompts.\nMeaningful pages.",
             closer="She's Glowing is a journal for pregnancy, birth and early motherhood, with gentle prompts, space to reflect and room for whatever today looks like."),
    ]
    return out
