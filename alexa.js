var info = "Things for Alexa was developed by Joe Shuff, and the latest update was released 22nd January 2017"

var intro = "Welcome to the game of things. This is made for groups of friends looking to have fun. To get a thing, say. Alexa, ask things for a thing"

var things = ["Things cannibals think about while dinning",
              "Things dogs are actually saying when they bark",
              "Things grown-ups wish they could still do....",
              "Things you should never put in your mouth...",
              "Things not to do in a hospital...",
              "Things not to do while driving!!...",
              "Things not to tell your mother...",
              "Things paramedics shouldn't say to a patient on the way to the hospital...",
              "Things people do when no one is looking...",
              "Things that are good!...",
              "Things that are harder than they look...",
              "Things that are your favorite foods!!...",
              "Things that you can use for transport (car, bike, bus, plane etc)...",
              "Things that confirm your house is haunted!...",
              "Things that confirm your life is going downhill...",
              "Things that go bad...",
              "Things that happen in vegas that should stay in vegas!!...",
              "Things that jiggle...",
              "Things that make sex fun!!!...",
              "Things that make you feel stupid!...",
              "Things that make you giggle!!!...",
              "Things that make you uncomfortable...",
              "Things that must be magic....",
              "Things that shouldn't be made into video games!!!...",
              "Things that shouldn't be passed from one generation to the next...",
              "Things that smell terrible...",
              "Things that squirt...",
              "Things that you will find in (name room of house..bathroom, kitchen, etc)...",
              "Things that you can trip over...",
              "Things that you love to watch on tv!...",
              "Things that you shouldn't do in public....",
              "Things that you shouldn't swallow....",
              "Things that you shouldn't throw off of a building....",
              "Things that your parents would kill you for....",
              "Things that would be fun to do in an elevator...",
              "Things that would keep you out of heaven...",
              "Things to wear to (occasion ...wedding, funeral, etc)...",
              "Things wouldn't want to be allergic to...",
              "Things you can never find...",
              "Things you do to get a job!...",
              "Things you do to relieve stress!...",
              "Things you do to stay warm!!!...",
              "Things you don't want to find in your bed...",
              "Things you might find in a library...",
              "Things you name home brewed beer!...",
              "Things you return from your christmas gifts......",
              "Things you shop for on black friday!...",
              "Things you should be thankful for!!...",
              "Things you should do to get ready for winter!!!...",
              "Things you should give as birthday gifts!...",
              "Things you should never put in your mouth....",
              "Things you shouldn't attempt to juggle...",
              "Things you shouldn't celebrate on your birthday!...",
              "Things you shouldn't do babysitting!!...",
              "Things you shouldn't do in public!...",
              "Things you shouldn't do on your birthday!!...",
              "Things you shouldn't do when naked...",
              "Things you shouldn't do with glue...",
              "Things you shouldn't give trick-or-treaters!!!...",
              "Things you shouldn't lick...",
              "Things you shouldn't play catch with....",
              "Things you shouldn't say to your in-laws...",
              "Things you shouldn't say when trying to make a good impression...",
              "Things you shouldn't say when walking out of the bathroom!!...",
              "Things you shouldn't send your friends in a pic!!!...",
              "Things you shouldn't swallow...",
              "Things you shouldn't throw off a building...",
              "Things you shouldn't tie to the roof of your car...",
              "Things you shouldn't wear to a wedding/ funeral...",
              "Things you shouldn't carve into a pumpkin!!...",
              "Things you use to remove snow from your car!...",
              "Things you wish for!...",
              "Things you wish were included in a divorce settlement!...",
              "Things you would ask a psychic...",
              "Things you would buy if you were rich!!!...",
              "Things you would do if you were a giant...",
              "Things you would rather forget...",
              "Things you would rather put off till tomorrow!!...",
              "Things you would wish for if you were stranded on an island!!...",
              "Things you wouldn't do for a million dollars...",
              "Things you wouldn't want made into a movie!...",
              "Things you wouldn't want to do in cemetery...",
              "Things you'd rather forget!...",
              "Things your friends text you!!...",
              "Things your parents forgot to tell you...",
              "Things your parents would kill you for...",
              "Things you shouldn't throw off a building!...",
              "Things you'll do when you retire...",
              "Things that would get a doctor sued for malpractice...",
              "Things you shouldn't do in front of a crowd...",
              "Things that give you a headache...",
              "Things you wouldn't want to clean...",
              "Things children shouldn't know...",
              "Things a gentleman shouldn't do...",
              "Things women know more about than men...",
              "Things you shouldn't give as a gift...",
              "Things that make you go ahhhh...",
              "Things you shouldn't do at the dinner table...",
              "Things you would consider strange to include on a resume...",
              "Things there should be an award for...",
              "Things people do when no one is looking...",
              "Things you shouldn't do when havig dinner with the Queen...",
              "Things you shouldn't make fun of...",
              "Things that make you giggle...",
              "Things you shouldn't teach your pets to do...",
              "Things you shouldn't photograph...",
              "Things you shouldn't do in the office...",
              "Things that make ballet more exciting...",
              "Things men know more about then women...",
              "Things you would say to a pig if it could talk...",
              "Things you can do to get rid of unwanted guests...",
              "Things you notice about yourself as you get older...",
              "Things you shouldn't say to your husband...",
              "Things you would line up to see...",
              "Thigns you shouldn't pay any attention to...",
              "Things a chicken thinks about when the farmer picks up the eggs...",
              "Things that make a good punch line...",
              "Things you wish grew on trees...",
              "Things you shouldn't say to you dentist...",
              "Thigns that confirm you are guilty...",
              "Thigns that tire you out...",
              "Things that confirm your house is haunted...",
              "Things you wish you could borrow from a library...",
              "Things you shouldn't do while writing a final exam...",
              "Things you shouldn't teach your parrot to say...",
              "Things that go bad...",
              "Things that shouldn't go into a time capsule...",
              "Things that hurt your back...",
              "Things you shouldn't mix...",
              "Things you just cant believe...",
              "Things that are politically incorrect...",
              "Things that happen once in a blue moon...",
              "Things about women that frustrate you...",
              "Things that are harder than they look...",
              "Things kids know more about than adults...",
              "Things that cause trouble...",
              "Things that make you relax...",
              "Things you wouldn't want to be allergic to...",
              "Things you shouldn't shout at the top of your lungs...",
              "Things you need to survive...",
              "Things you shouldn't do in a car...",
              "Things you would like to play with...",
              "Things you can't stop...",
              "Things you shouldn't do on vacation...",
              "Things you would wish for if you found a genie in a bottle...",
              "Things that seem to take an eternity...",
              "Things that confirm you are losing your memory...",
              "Things you shouldn't display in your china cabinet...",
              "Things you would like as your last words...",
              "Things that shouldn't be passed from one generation to the next...",
              "Things firemen do between fires...",
              "Things you shouldn't put off until tomorrow...",
              "Things that shouldn't be lumpy...",
              "Things fish think about as they swim in their aquarium...",
              "Things that confirm that your life is going downhill...",
              "Things you could use as an excuse on judgement day...",
              "Things that would make golf more exciting...",
              "Things you shouldn't advertise in the classified ads...",
              "Things you shouldn't do in the house...",
              "Things that would make work more exciting...",
              "Things that are wild...",
              "Things that require an assistant...",
              "Things you would like to say to the President...",
              "Things you would like to ask a psychic...",
              "Things you shouldn't encourage your children to do...",
              "Things you wish you could do with your feet...",
              "Things you never see on television...",
              "Things you wish worked by remote control...",
              "Things you shouldn't exaggerate...",
              "Things a waiter shouldn't do...",
              "Things you shouldn't collect...",
              "Things that confirm you still haven't grown up...",
              "Things you shouldn't touch...",
              "Things you shouldn't attempt at your age...",
              "Things that confirm your small town is backward...",
              "Things that would make school more exciting...",
              "Things you shouldn't tie to the roof of your car...",
              "Things you shouldn't send in the mail...",
              "Things that usually make you feel better...",
              "Things you would like to do on vacation...",
              "Things you would have said to Eve had she tricked you into eating the apple...",
              "Things that cause an accident...",
              "Things you shouldn't say to get out of a speeding ticket...",
              "Things you shouldn't say about your children...",
              "Things you shouldn't hold while riding a bike...",
              "Things you wish you could predict...",
              "Things that hurt...",
              "Things you shouldn't give away...",
              "Things you hate as punishment...",
              "Things you shouldn't advertise on a billboard...",
              "Things that are embarrassing...",
              "Things you shouldn't do in public...",
              "Things that require a lot of patience...",
              "Things you shouldn't say to your boss...",
              "Things you shouldn't let an amateur do...",
              "Things you wish you could erase...",
              "Things you say to a telemarketer...",
              "Things you wouldn't want to find in your sandwich...",
              "Things you shouldn't put in your mouth...",
              "Things you shouldn't do at a funeral...",
              "Things that exhaust you...",
              "Things you shouldn't do at the theatre...",
              "Things you shouldn't do in the bathtub...",
              "Things you shouldn't write on a Valentine's card...",
              "Things you shouldn't say to your grandmother...",
              "Things that make you jump...",
              "Things you won't find in a dictionary...",
              "Things you shouldn't say to a flight attendant...",
              "Things you shouldn't put on the front lawn...",
              "Things that drive you mad...",
              "Things that jiggle...",
              "Things you shouldn't do in your backyard...",
              "Things you wouldn't want to find in your Christmas stocking...",
              "Things you wish people would stop talking about...",
              "Things you just can't beat...",
              "Things you shouldn't call your children...",
              "Things you shouldn't do with your mouth open...",
              "Things that would make your love life more exciting...",
              "Things you shouldn't do at a party...",
              "Things that are dirty...",
              "Things you've paid too much for...",
              "Things you call your mate...",
              "Things you shouldn't swallow...",
              "Things you shouldn't laugh at...",
              "Things you should keep to yourself...",
              "Things you wouldn't want your mother to talk about with your girlfriend/boyfriend...",
              "Things you shouldn't do on your desk...",
              "Things you would like to do in a blackout...",
              "Things that make you cry...",
              "Things you would do if you had super-human powers...",
              "Things that are naughty...",
              "Things that make you go ooooh...",
              "Things that really need a referee...",
              "Things you shouldn't put on the kitchen table...",
              "Things you shouldnt do in a hospital...",
              "Things you shouldn't say to a police officer...",
              "Things you shouldn't lick...",
              "Things you would do if you changed genders for a day...",
              "Things you wouldn't do for all the money in the world...",
              "Things you would rather forget...",
              "Things dogs are actually saying when they bark...",
              "Things that would be considered a bad habit...",
              "Things you would rather be doing right now...",
              "Things you shouldn't bite...",
              "Things you shouldn't say to your in-laws...",
              "Things astronauts complain about in space...",
              "Things you shouldn't do with your tongue...",
              "Things you wouldn't want to know about your grandmother...",
              "Things that make you gag...",
              "Things about men that frustrate you...",
              "Things you shouldn't say to your mother...",
              "Things a chimp thinks about when he sees you at the zoo...",
              "Things an ideal mate would do for you...",
              "Things you shouldn't forget...",
              "Things a doctor shouldn't do while performing surgery...",
              "Things you shouldn't say to the First Lady...",
              "Things you shouldn't do with glue...",
              "Things you hate about the hospital...",
              "Things that should have an expiration date...",
              "Things you shouldn't do at the beach...",
              "Things people like about you...",
              "Things you shouldn't say to your doctor...",
              "Things that confirm you are losing your mind...",
              "Things that dont last very long...",
              "Things you didn't realize until it was too late...",
              "Things that confirm you have had to much to drink...",
              "Things you keep hidden...",
              "Things you would like to see in your horoscope...",
              "Things you shouldn't lend...",
              "Things that take courage...",
              "Things you shouldn't say to your teacher...",
              "Things you shouldn't do right after you eat...",
              "Things you shouldn't do on your first day on the job...",
              "Things you shouldn't throw off a building...",
              "Things you shouldn't do at the circus...",
              "Things you shouldn't capture on videotape...",
              "Things women talk about when they go to the restroom together...",
              "Things that should come with a manual...",
              "Things you shouldn't do on a first date...",
              "Things that hang...",
              "Things that confirm you have been abducted by aliens...",
              "Things you never see in the country...",
              "Things you shouldn't try to hold on to...",
              "Things a cow thinks about when a farmer milks it...",
              "Things that prove you're in a bad restaurant...",
              "Things you shouldn't say in group therapy...",
              "Things that could get you arrested...",
              "Things children shouldn't play with...",
              "Things you shouldn't say to your father...",
              "Things you want to do before you die...",
              "Things you know nothing about...",
              "Things a lady shouldn't do...",
              "Thigns you dream about...",
              "Things that confirm your car is a lemon...",
              "Things that could result in a war...",
              "Things you shouldn't say to your wife...",
              "Things you would have a robot do...",
              "Things cats think about humans...",
              "Things you would do if you were a dictator...",
              "Things you would like to change...",
              "Things you would do if you were a giant...",
              "Things you shouldn't pick up...",
              "Things that would make meetings more exciting...",
              "Things you never remember...",
              "Things you keep in your car...",
              "Things you shouldn't doodle on...",
              "Things that don't make sense...",
              "Things you wish you could do in your sleep...",
              "Things you would like to study...",
              "Thigns that would get you sent to the Principal's office...",
              "Things you might complain about in Hell...",
              "Things you shouldn't celebrate...",
              "Things you hope you can still do when you are 85...",
              "Things you shouldn't do when you are naked...",
              "Things you shouldn't share...",
              "Thigns that are none of your business...",
              "Things you will never see in your lifetime...",
              "Things that could spoil your appetite...",
              "Things you don't like about family gatherings...",
              "Things that could use a good cleaning...",
              "Things you shouldn't do on an airplane...",
              "Things that make you uncomfortable...",
              "Things that must be magic...",
              "Things you shouldn't attempt to juggle...",
              "Things that are funny...",
              "Things you shouldn't do on your honeymoon...",
              "Things you hate to be called...",
              "Things that would get you discharged from the army...",
              "Things you would like to make someone do under hypnosis...",
              "Things you shouldn't title a children's book...",
              "Things that don't exist but you wish they did...",
              "Things you shouldn't do with a computer...",
              "Things you would like to do with a bald head...",
              "Things that make you scream...",
              "Things that would get you fired...",
              "Things that warrant an apology...",
              "Things you shouldn't do in the shower...",
              "Things you would hate to do for a living...",
              "Things you shouldn't leave open...",
              "Things that very old people shouldn't do...",
              "Things you shouldn't do if you want to make a good first impression...",
              "Things big dogs think about when they see a Chihuahua...",
              "Things that make you feel young...",
              "Things you shouldn't play catch with...",
              "Things you shouldn't say to your troops before they go to battle...",
              "Things you wish you didn't know...",
              "Things you shouldn't use as an opening line...",
              "Things that make people jealous...",
              "Things you would like to add to the Ten Commandments...",
              "Things you love to shop for...",
              "Things you shouldn't try to do in the dark...",
              "Things you would do if you were invisible...",
              "Things you shouldn't do in a group of people...",
              "Things you can't believe someone actually did...",
              "Things that make you angry...",
              "Things you shouldn't have to pay for...",
              "Things you wish had been taught in school...",
              "Things that make you nervous...",
              "Things you wish were delivered...",
              "Things you would like to wake up to...",
              "Things you shouldn't do in a cemetery...",
              "Things that are impossible to measure...",
              "Things you shouldn't do at your wedding...",
              "Things that are better late than never...",
              "Things you never see in the city...",
              "Things that would probably keep you out of heaven...",
              "Things you would like to try...",
              "Things you shouldn't do while golfing...",
              "Things you shouldn't experiment with...",
              "Things that are useless...",
              "Things you shouldn't do on a bus...",
              "Things you would like to do with chocolate...",
              "Things you shouldn't say to break the silence in a conversation...",
              "Things you would do with a million dollars...",
              "Things you wish you could buy out of vending machines...",
              "Things you shoudn't do at a job interview...",
              "Things you shouldn't accept from strangers...",
              "Things you shouldn't do quickly..."]

exports.handler = (event, context) => {

  try {

    if (event.session.new) {
      // New Session
      console.log("NEW SESSION")
    }

    switch (event.request.type) {

      case "LaunchRequest":
        // Launch Request
        console.log(`LAUNCH REQUEST`)
        context.succeed(generateResponse(buildSpeechletResponse(intro, true),{}))
        break;

      case "IntentRequest":
        // Intent Request
        console.log(`INTENT REQUEST`)

        switch(event.request.intent.name) {
          case "GetThing":
            var thing = things[Math.floor(Math.random()*things.length)];
            var userId = event.session.user.userId;
            //savetoDB(thing, userId);
            context.succeed(generateResponse(buildSpeechletResponse(thing, true),{}))
            break;
        
          case "AmountOfThings":
            context.succeed(generateResponse(buildSpeechletResponse("There are " + things.length + " things", true),{}))
            break;
            
          case "InfoThings":
            context.succeed(generateResponse(buildSpeechletResponse(info, true),{}))
            break;
            
          default:
            throw "Invalid intent"
        }

        break;

      case "SessionEndedRequest":
        // Session Ended Request
        console.log(`SESSION ENDED REQUEST`)
        break;

      default:
        context.fail(`INVALID REQUEST TYPE: ${event.request.type}`)

    }

  } catch(error) { context.fail(`Exception: ${error}`) }

}

// var dynasty = require('dynasty')({});
// var dataTable = function(){
    // return dynasty.table('thingsData');
// };

function saveToDb(thing, id) {
    dataTable().insert({
        userId: id,
        Data: JSON.stringify(thing)
    });
}

function loadFromDb(id) {
    
    dataTable().find(id)
        .then(function(result) {
            var data = {};
            
            if (result !== undefined){
                data = JSON.parse(result['data']);
            }
            
            return data
        }).catch(function(error) {});
}

// Helpers
buildSpeechletResponse = (outputText, shouldEndSession) => {

  return {
    outputSpeech: {
      type: "PlainText",
      text: outputText
    },
    shouldEndSession: shouldEndSession
  }

}

generateResponse = (speechletResponse, sessionAttributes) => {

  return {
    version: "1.0",
    sessionAttributes: sessionAttributes,
    response: speechletResponse
  }

}