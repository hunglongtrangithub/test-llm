  function iaf(txt) {
    var aff=txt.replace( /AFF_/g,"<br><h3>Affirmed</h3>" );
    var neg=aff.replace( /NEG_/g,"<br><h3>Negated</h3>" );
    var unc=neg.replace( /UNC_/g,"<br><h3>Uncertain</h3>" );
    var unn=unc.replace( /UNN_/g,"<br><h3>Uncertain, Negated</h3>" );
    var gnr=unn.replace( /GNR_/g,"" );
    var wik1=gnr.replace( /WIK_/g,"<a href=\"https://vsearch.nlm.nih.gov/vivisimo/cgi-bin/query-meta?v%3Aproject=medlineplus&v%3Asources=medlineplus-bundle&query=" );
    var wik2=wik1.replace( /_WK_/g,"\" target=\"_blank\">" );
    var wik3=wik2.replace( /_WIK/g,"</a>" );
    var _drg_=wik3.replace( /_DRG_/g,"<b>Drug</b>" );
    var _dis_=_drg_.replace( /_DIS_/g,"<b>Disorder</b>" );
    var _fnd_=_dis_.replace( /_FND_/g,"<b>Finding</b>" );
    var _prc_=_fnd_.replace( /_PRC_/g,"<b>Procedure</b>" );
    var _ant_=_prc_.replace( /_ANT_/g,"<b>Anatomy</b>" );
    var _att_=_ant_.replace( /_ATT_/g,"<b>Attribute</b>" );
    var _dev_=_att_.replace( /_DEV_/g,"<b>Device</b>" );
    var _lab_=_dev_.replace( /_LAB_/g,"<b>Lab</b>" );
    var _phn_=_lab_.replace( /_PHN_/g,"<b>Phenomenon</b>" );
    var _sbj_=_phn_.replace( /_SBJ_/g,"<b>Subject</b>" );
    var _ttl_=_sbj_.replace( /_TTL_/g,"<b>Title</b>" );
    var _evt_=_ttl_.replace( /_EVT_/g,"<b>Event</b>" );
    var _ent_=_evt_.replace( /_ENT_/g,"<b>Entity</b>" );
    var _tmx_=_ent_.replace( /_TMX_/g,"<b>Time</b>" );
    var _mod_=_tmx_.replace( /_MOD_/g,"<b>Modifier</b>" );
    var _labm_=_mod_.replace( /_LABM_/g,"<b>LabModifier</b>" );
    var _unk_=_labm_.replace( /_UNK_/g,"<b>Unknown</b>" );
    var spc=_unk_.replace( /SPC_/g,"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" );
    var prf1=spc.replace( /\[/g,"<i>" );
    var prf2=prf1.replace( /\]/g,"</i>" );
    var nl=prf2.replace( /NL_/g,"<br>" );
    document.getElementById("ia").innerHTML = nl;
  }
