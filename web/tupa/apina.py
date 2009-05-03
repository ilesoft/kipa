
from models import *
from django.forms import ModelForm
from django import forms

class apina(ModelForm) :
    nimi = forms.CharField() 
    def __init__(self,tehtava,*argv,**argkw) :
        super(ModelForm,self).__init__(*argv,**argkw)
        self.tehtava=tehtava
    def tallenna(self):
        kaava = super(ModelForm,self).save(commit=False)
        kaava.tehtava = self.tehtava
        kaava.nimi= self.cleaned_data['nimi']
        return kaava
    class Meta:
        exclude = ('tehtava','kaava')
        model = OsapisteKaava

psChoices= (("p","pienin"),("s","suurin"))
tyyppiChoices= (("piste","piste"),("aika","aika"))
kerroinChoices =(("1.5","1.5 (pienin tulos saa parhaat)"),("0.5","0.5 (suurin tulos saa parhaat pisteet)"))

class interpoloi(apina):
    tyyppi = forms.ChoiceField(choices=tyyppiChoices)
    jaettavat_pisteet = forms.FloatField()
    kerroin = forms.ChoiceField(choices=kerroinChoices,widget=forms.RadioSelect)
    def save(self):
        kaava = self.tallenna()
        maariteet = SyoteMaarite.objects.filter(tehtava=self.tehtava).filter(nimi="op_"+kaava.nimi)
        maarite=None
        if not maariteet :
            maarite = SyoteMaarite()
        else : 
            maarite = maaritteet[0]
        maarite.nimi="op_"+kaava.nimi
        maarite.tehtava = self.tehtava
        maarite.tyyppi=self.cleaned_data['tyyppi']
        
        maksimi=None
        if self.cleaned_data['kerroin'] == "0.5" :
            maksimi = "s"
        elif self.cleaned_data['kerroin'] == "1.5" :
            maksimi = "p"

        kaava.kaava = "interpoloi(" +maarite.nimi +"," 
        kaava.kaava = kaava.kaava + self.cleaned_data['kerroin'] 
        kaava.kaava = kaava.kaava + ",med,"+ maksimi +"," + str(self.cleaned_data['jaettavat_pisteet']) + ")"
        kaava.save()
        maarite.save()
    
class raakapiste(apina):
    syotteita= forms.IntegerField()
    raakapisteita_yhteensa=forms.FloatField()
    jaettavat_pisteet = forms.FloatField()
    def save(self):
        kaava = self.tallenna()
        maaritteet = []
        maara = self.cleaned_data['syotteita']
        kaava.kaava = "("
        for i in range(maara):
                maarite = SyoteMaarite()
                maarite.nimi = "rp_" + kaava.nimi + str(i)
                maarite.tehtava=self.tehtava
                maarite.tyyppi="piste"
                maarite.save()
                kaava.kaava=kaava.kaava + maarite.nimi + "+"
        rp_yht=self.cleaned_data['raakapisteita_yhteensa']
        kaava.kaava=kaava.kaava[:-1]+")/"+str(rp_yht)+"*"+str(self.cleaned_data['jaettavat_pisteet'] )
        kaava.save()
            

