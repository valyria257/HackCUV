
var card_faces= ["AC.png", "2C.png", "3C.png", "4C.png", "5C.png", "6C.png", "7C.png", "8C.png", 
"9C.png", "10C.png", "JC.png", "QC.png", "KC.png", "AH.png", "2H.png", "3H.png", "4H.png", "5H.png", "6H.png", "7H.png", "8H.png", 
"9H.png", "10H.png", "JH.png", "QH.png", "KH.png", "AS.png", "2S.png", "3S.png", "4S.png", "5S.png", "6S.png", "7S.png", "8S.png",
"9S.png", "10S.png", "JS.png", "QS.png", "KS.png", "AD.png", "2D.png", "3D.png", "4D.png", "5D.png", "6D.png", "7D.png", "8D.png",
"9D.png", "10D.png", "JD.png", "QD.png", "KD.png"];


function flipCard(){
	
	//deals random cards
	rand_num = Math.floor(Math.random() * 52);
	document.getElementById("card1").src=card_faces[rand_num];
	console.log(rand_num)
	console.log(card_faces[rand_num]);
}
