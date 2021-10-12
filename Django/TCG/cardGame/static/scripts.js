//import { refreshHand, refreshBench, refreshActive } as monModule from './static/refresh.js';

//------------------------------------------------
//--- Dessine le banc
//------------------------------------------------
function refreshBench(pos, isPlayer){
  type = "adversaireCarteBanc"
  if (isPlayer){
    type = "joueurCarteBanc"
  }

  $.ajax({
    url: 'http://localhost:8000/refreshBench/'+pos+"/"+isPlayer,
    //data: { "carteMain": , "zoneVide": },
    type: 'get',
    async: false,
    statusCode: {
      200: function(content) {
        //alert("refresh bench");
        oldImg = $("#"+pos+"."+type)
        $(oldImg).after(content);
        $(oldImg).remove();
      }
    }
  });
}

//------------------------------------------------
//--- Dessine le pokemon actif
//------------------------------------------------
function refreshActive(pos, isPlayer){
  type = "zoneCarteActif"
  type2 = "adversaireCartePokemonActif"
  if (isPlayer){
    type = "zoneCarteActif"
    type2 = "joueurCartePokemonActif"
  }

  $.ajax({
    url: 'http://localhost:8000/refreshActive/'+pos+"/"+isPlayer,
    //data: { "carteMain": , "zoneVide": },
    type: 'get',
    async: false,
    statusCode: {
      200: function(content) {
        //alert("refresh bench");
        var oldImg = $("#"+pos+"."+type)
        var oldImg2 = $("#"+pos+"."+type2)
        //alert("oldImg="+$("#"+pos+"."+type)+" ___ "+$(oldImg).html())
        $(oldImg).after(content);
        $(oldImg).remove();
        $(oldImg2).after(content);
        $(oldImg2).remove();
      }
    }
  });
}

//------------------------------------------------
//--- Dessine la main du joueur
//------------------------------------------------
function refreshHand2(isPlayer){
  type = "adversaireCarte"
  container = "mainAdversaire"
  if (isPlayer){
    type = "joueurCarte"
    container = "mainJoueur"
  }

  //alert("type : "+type+" container : "+container)

  $.ajax({
    url: 'http://localhost:8000/refreshHand/'+isPlayer,
    //data: { "carteMain": , "zoneVide": },
    type: 'get',
    async: false,
    statusCode: {
      200: function(content) {
        //remplacement
        $("."+container).children().remove()
        $("."+container).html(content)

        //events
        $(".flecheAvant").on( "click", actionFlecheAvant);
        $(".flecheArriere").on( "click", actionFlecheArriere);
        $('.'+type).click(function() {
          changeSelection($(this).attr("id"),type)
        })
      }
    }
  });
}

//------------------------------------------------
//--- Dessine les pv
//------------------------------------------------
function refreshPv2(pos, type, isPlayer){
  img = $("#"+pos+"."+type)
  oldPv = $(img).parent().find(".pvIcon")
  $.ajax({
    url: 'http://localhost:8000/refreshPv/'+type+"/"+pos+"/"+isPlayer,
    //data: { "carteMain": , "zoneVide": },
    type: 'get',
    async: false,
    statusCode: {
      200: function(content) {
        //alert("success refresh");
        $(img).after(content);
        $(oldPv).remove();
      }
    }
  });
}

//------------------------------------------------
//--- Dessine le modal d'actions
//------------------------------------------------
function refreshModal(pos, type){
  $.ajax({
    url: 'http://localhost:8000/refreshModalPlayer/'+type+"/"+pos,
    //data: { "carteMain": , "zoneVide": },
    type: 'get',
    async: false,
    statusCode: {
      200: function(content) {
        //remplacement
        $(".actionPanneau").remove()
        $(".attaquePanneau").remove()
        $(".selected").after(content)

        //events
        $(".pokePower").on( "click", {pos:pos,type:type}, actionPokePower);
        $(".retraite").on( "click", actionRetraite);
        if(type == "joueurCartePokemonActif"){
          //attaques events
          $(".attaque").on( "click", {id:0}, actionAttaque);
        }
      }
    }
  });
}

//------------------------------------------------
//--- Dessine la main du joueur
//------------------------------------------------
// function refreshHand(content){
//   $(".mainJoueur").children().remove()
//   $(".mainJoueur").html(content)
//   $(".flecheAvant").on( "click", actionFlecheAvant);
//   $(".flecheArriere").on( "click", actionFlecheArriere);
//   $('.joueurCarte').click(function() {
//     changeSelection($(this).attr("id"),"joueurCarte")
//   })
// }

//------------------------------------------------
//--- Dessine les pv
//------------------------------------------------
function refreshPv(pos, type){
  select = $("#"+pos+"."+type)
  pv = $(select).parent().find(".pvIcon")
  $.ajax({
    url: 'http://localhost:8000/refreshPv/'+type+"/"+pos+"/1",
    //data: { "carteMain": , "zoneVide": },
    type: 'get',
    async: false,
    statusCode: {
      200: function(content) {
        $(select).after(content);
        $(pv).remove();
      }
    }
  });
}

//------------------------------------------------
//--- Dessine le modal d'actions
//------------------------------------------------
// function drawModal(pos, type){
//   $.ajax({
//     url: 'http://localhost:8000/refreshModalPlayer/'+type+"/"+pos,
//     //data: { "carteMain": , "zoneVide": },
//     type: 'get', // This is the default though, you don't actually need to always mention it
//     statusCode: {
//       200: function(content) {
//         $(".selected").after(content)
//         $(".pokePower").on( "click", {pos:pos,type:type}, actionPokePower);
//         $(".retraite").on( "click", actionRetraite);
//         if(type == "joueurCartePokemonActif"){
//           //attaques events
//         }
//       }
//     }
//   });
// }

//----------------------------------------------------------------------------------------------------------------------------------------

//------------------------------------------------
//--- Click sur une fleche avant
//------------------------------------------------
function actionFlecheAvant(){
  $.ajax({
    url: 'http://localhost:8000/flecheAvant',
    //data: { "carteMain": , "zoneVide": },
    type: 'get',
    async: false,
    statusCode: {
      200: function(content) {
          refreshHand2(1)
      }
    }
  });
};

//------------------------------------------------
//--- Click sur une fleche avant
//------------------------------------------------
function actionFlecheArriere(){
  $.ajax({
    url: 'http://localhost:8000/flecheArriere',
    //data: { "carteMain": , "zoneVide": },
    type: 'get',
    async: false,
    statusCode: {
      200: function(content) {
          refreshHand2(1)
      }
    }
  });
};

//------------------------------------------------
//--- Click sur le bouton pokePower
//------------------------------------------------
function actionPokePower (event){
  $.ajax({
    url: 'http://localhost:8000/pokePower/'+event.data.type+'/'+event.data.pos,
    //data: { "carteMain": , "zoneVide": },
    type: 'get',
    async: false,
    statusCode: {
      200: function(content) {
        $(".pokePower").addClass("invisible")
        refreshHand2(1)
      }
    }
  });
};

//------------------------------------------------
//--- Click sur le bouton retraite
//------------------------------------------------
function actionRetraite (){
  $.ajax({
    url: 'http://localhost:8000/retraite',
    type: 'get',
    async: false,
    statusCode: {
      200: function(content) {
        retraite = $(".retraite")
        $(retraite).after(content)
        $(retraite).remove()
        $(".retraite").on( "click", actionRetraite);
      }
    }
  });
};

//------------------------------------------------
//--- Click sur une zone carte du banc
//------------------------------------------------
function actionJoueurCartePokemonActif(event){
  $.ajax({
    url: 'http://localhost:8000/echangeRetraite/joueurCartePokemonActif/'+event.data.id,
    //data: { "carteMain": , "zoneVide": },
    type: 'get',
    async: false,
    dataType: 'json',
    statusCode: {
      200: function(data) { //on etait en mode action : on bat en retraite
        activePkmn = $("#"+event.data.id+".joueurCartePokemonActif")
        benchedPkmn = $("#"+data["id"]+".joueurCarteBanc")

        var position1 = $(activePkmn).offset();
        var position2 = $(benchedPkmn).offset();

        $.when(
          $(benchedPkmn).animate({
            'top': (position1.top - position2.top) + 'px',
            'left': (position1.left - position2.left) + 'px'
          },1000).promise(),
          $(activePkmn).animate({
            'top': (position2.top - position1.top) + 'px',
            'left': (position2.left - position1.left) + 'px'
          },1000).promise()
        ).then(function() {

          //on force la suppression
          //$(activePkmn).remove()
          //$(benchedPkmn).remove()

          //on raffraichit pour faire apparaitre les vraies cartes echangees dans la view
          refreshActive(event.data.id,1)
          refreshBench(data["id"],1)

          //bug bizaroïde ?????
          //$("#"+event.data.id+".joueurCartePokemonActif").removeAttr("style")
          //$("#"+data["id"]+".joueurCarteBanc").removeAttr("style")

          //events
          $("#"+event.data.id+".joueurCartePokemonActif").on( "click", {id:event.data.id}, actionJoueurCartePokemonActif);
          $("#"+data["id"]+".joueurCarteBanc").on( "click", {id:data["id"]}, actionJoueurCarteBanc);

          //toogle mode action
          actionRetraite()
        });
      }
    }
  });
  changeSelection(event.data.id,"joueurCartePokemonActif")
};

//------------------------------------------------
//--- Click sur une zone carte du banc
//------------------------------------------------
function actionJoueurCarteBanc(event){
  changeSelection(event.data.id,"joueurCarteBanc")
};

//------------------------------------------------
//--- Click sur une zone carte du banc
//------------------------------------------------
function actionAttaque(event){
  $.ajax({
    url: 'http://localhost:8000/attaque/'+event.data.id,
    //data: { "carteMain": , "zoneVide": },
    type: 'get',
    async: false,
    dataType: 'json',
    statusCode: {
      200: function(data) {
        refreshPv2(0,"joueurCartePokemonActif",1)
        refreshPv2(0,"adversaireCartePokemonActif",0)
      }
    }
  });
};

//------------------------------------------------
//--- Click sur une zone carte pokemon actif
//------------------------------------------------
function actionZoneCarteActif(id){
  $.ajax({
    url: 'http://localhost:8000/joueCarte/'+"zoneCarteActif"+'/'+id,
    //data: { "carteMain": , "zoneVide": },
    type: 'get',
    async: false,
    dataType: 'json',
    statusCode: {
      200: function(data) {
        zoneCarteActive = $("#"+id+".zoneCarteActif")
        carteMain = $("#"+data["id"]+".joueurCarte")

        var position1 = $(zoneCarteActive).offset();
        var position2 = $(carteMain).offset();

        $.when(
          $(carteMain).animate({
            'top': (position1.top - position2.top) + 'px',
            'left': (position1.left - position2.left) + 'px'
          },1000).promise()
        ).done(function() {
          //on raffraichit pour faire apparaitre la carte jouee
          refreshActive(id,1)
          //$(zoneCarteActive).after(data["actif"])
          //$(zoneCarteActive).remove()

          activePkmn = $("#"+id+".joueurCartePokemonActif")

          refreshHand2(1)

          $(activePkmn).on( "click", {id:id}, actionJoueurCartePokemonActif);

          changeSelection(id,"joueurCartePokemonActif")
          refreshPv(id, "joueurCartePokemonActif")
        });
      }
    }
  });
};

//------------------------------------------------
//--- Click sur une zone carte du banc
//------------------------------------------------
function actionZoneCarteBanc(id){
  $.ajax({
    url: 'http://localhost:8000/joueCarte/'+"zoneCarteBanc"+'/'+id,
    //data: { "carteMain": , "zoneVide": },
    type: 'get',
    async: false,
    dataType: 'json',
    statusCode: {
      200: function(data) {
        //location.reload();
        select = $("#"+id+".zoneCarteBanc")
        $(select).after(data["banc"])
        $(select).remove()

        $("#"+id+".joueurCarteBanc").on( "click", {id:id}, actionJoueurCarteBanc);
        refreshHand2(1)

        changeSelection(id,"joueurCarteBanc")
        refreshPv(id, "joueurCarteBanc")
      }
    }
  });
};

//------------------------------------------------
//--- MAJ selection
//------------------------------------------------
function changeSelection(pos, type){

  $.ajax({
    url: 'http://localhost:8000/changeSelection/'+pos+'/'+type,
    //data: { "carteMain": , "zoneVide": },
    type: 'get',
    async: false,
    statusCode: {
      204: function(data) {
        $(".selected").removeClass("selected")
        $(document).find("#"+pos+"."+type).addClass("selected")

        refreshModal(pos,type)
      }
    }
  });
}

//------------------------------------------------
//--- Clicks sur carte par defaut
//------------------------------------------------
$(document).ready(function () {
  $('.joueurCarteBanc, .adversaireCarteBanc, .zoneCarteBanc, .zoneCarteActif, .joueurCartePokemonActif, .joueurCarte, .adversaireCarte, .flecheAvant, .flecheArriere').click(function() {

    if($(this).hasClass("joueurCarteBanc")){
      changeSelection($(this).attr("id"),"joueurCarteBanc")
    }else if($(this).hasClass("joueurCartePokemonActif")){
      changeSelection($(this).attr("id"),"joueurCartePokemonActif")
    }else if($(this).hasClass("adversaireCarteBanc")){
      changeSelection($(this).attr("id"),"adversaireCarteBanc")
    }else if($(this).hasClass("joueurCarte")){
      changeSelection($(this).attr("id"),"joueurCarte")
    }else if($(this).hasClass("adversaireCarte")){
      changeSelection($(this).attr("id"),"adversaireCarte")
    }else if($(this).hasClass("flecheAvant")){
      actionFlecheAvant()
    }else if($(this).hasClass("flecheArriere")){
      actionFlecheArriere()
    }else if($(this).hasClass("zoneCarteBanc")){
      actionZoneCarteBanc($(this).attr("id"))
    }else if($(this).hasClass("zoneCarteActif")){
      actionZoneCarteActif($(this).attr("id"))
    }
  })
})

//------------------------------------------------
//--- AJAX bouton
//------------------------------------------------
$(document).ready(function () {
  $('#b1').click(function() {
    $.ajax({
      url: 'http://localhost:8000/test',
      type: 'get', // This is the default though, you don't actually need to always mention it
      success: function(content) {
          //alert(data);
          //location.reload();

          refreshHand2(1)
          refreshHand2(0)
          // $.when().then(function( data, textStatus, jqXHR ) {
          //   alert( jqXHR.status ); // Alerts 200
          //
          // });

      }
    });
  })
})
