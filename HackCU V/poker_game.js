
var card_faces= ["2H.png", "3H.png", "4H.png", "5H.png", "6H.png", "7H.png", "8H.png","9H.png", "10H.png", "JH.png", "QH.png", "KH.png","AH.png",
"2D.png", "3D.png", "4D.png", "5D.png", "6D.png", "7D.png", "8D.png","9D.png", "10D.png", "JD.png", "QD.png", "KD.png", "AD.png",
"2C.png", "3C.png", "4C.png", "5C.png", "6C.png", "7C.png", "8C.png", "9C.png", "10C.png", "JC.png", "QC.png", "KC.png", "AC.png",
"2S.png", "3S.png", "4S.png", "5S.png", "6S.png", "7S.png", "8S.png","9S.png", "10S.png", "JS.png", "QS.png", "KS.png","AS.png"];


class Poker{

        constructor(){
          this.players = [
            {name:"A", chips:1000, bet:0},
            {name:"B", chips:1000, bet:0},
            {name:"C", chips:1000, bet:0},
            {name:"D", chips:1000, bet:0}
          ]
          this.playerRef = document.getElementById("playerTable");
          this.tableRef = document.getElementById("tableData");
        }

        updateTable(){
          var html = "<tr><th>Name</th><th>Chips</th><th>Bet</th></tr>"
          for(var i = 0; i < this.players.length; i++){
            html += "<tr><td>"+this.players[i].name
                  + "</td><td>"+this.players[i].chips
                  + "</td><td>"+this.players[i].bet
                  + "</td></tr>";
          }
          this.playerRef.innerHTML = html;
        }

        addCardToTable(){
          this.tableRef.innerHTML += "<span>Hearts King</span>";
        }
      }

var first_card_flipped = false;
var all_cards_filled = false;
let poker_game;

function dealCards(){
	poker_game = new Poker();

	//your cards
	var rand_num = Math.floor(Math.random() * 52);
	document.getElementById("card6").src=card_faces[rand_num];
	card_faces.splice(rand_num, 1);
	Math.floor(Math.random() * 51);
	document.getElementById("card7").src=card_faces[rand_num];
	card_faces.splice(rand_num, 1);



	//table cards
	rand_num = Math.floor(Math.random() * 50);
	document.getElementById("card1").src=card_faces[rand_num];
	card_faces.splice(rand_num, 1);
	rand_num = Math.floor(Math.random() * 49);
	document.getElementById("card2").src=card_faces[rand_num];
	card_faces.splice(rand_num, 1);
	rand_num = Math.floor(Math.random() * 48);
	document.getElementById("card3").src=card_faces[rand_num];
	card_faces.splice(rand_num, 1);
}



function flipCard(){
	//deals random cards
	if(!first_card_flipped && !all_cards_filled){
		rand_num = Math.floor(Math.random() * 47);
		document.getElementById("card4").src=card_faces[rand_num];
		card_faces.splice(rand_num, 1);
		first_card_flipped = true;
	}else if(first_card_flipped && !all_cards_filled){
		rand_num = Math.floor(Math.random() * 46);
		document.getElementById("card5").src=card_faces[rand_num];
		card_faces.splice(rand_num, 1);
		all_cards_filled = true;
		var element = document.getElementById("flipButton");
  		element.classList.add("hidden");
	}else{
		//do nothing
	}	
	
}


function fillPot(){
	poker_game.updateTable();
	document.getElementById("pot").innerHTML += 1;
	poker_game.players[1].bet += 1;
	poker_game.updateTable();
}






