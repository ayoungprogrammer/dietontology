from flask import Flask, render_template, request
from owlready2 import *


def get_leaves(ent):
    subc = list(ent.subclasses())
    if len(subc) == 0:
        return [ent]
    res = []
    for c in subc:
        res += get_leaves(c)
    return res


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def get_foods():

    print(request.form)

    fg = request.form.get('foodGroups', 'all')


    world = World()
    onto = world.get_ontology("file:///Users/myoung/Documents/bmi210/project/nutrients.owl").load()
    with onto:
        equiv = onto.Food
        if fg == 'dairy':
            equiv = onto.Dairy
        elif fg == 'fruits':
            equiv = onto.Fruits
        elif fg == 'grains':
            equiv = onto.Grains
        elif fg == 'proteins':
            equiv = onto.Proteins
        elif fg == 'vegetables':
            equiv = onto.Vegetables
        elif fg == 'all':
            equiv = onto.Food


        if request.form.get('vegan'):
            equiv = equiv & onto.VeganFood

        if request.form.get('vegetarian'):
       	    equiv = equiv & onto.VegetarianFood

        if request.form.get('pescetarian'):
            equiv = equiv & onto.PescetarianFood

        if request.form.get('gluten_free'):
       	    equiv = equiv & onto.GlutenIntoleranceFood

        if request.form.get('lactose_intolerant'):
            equiv = equiv & onto.LactoseIntoleranceFood

        if request.form.get('cholestrol_restricted'):
            equiv = equiv & onto.Cholestrol_Restricted_Food

        if request.form.get('egg_allergy'):
            equiv = equiv & Not(onto.hasAllergy.some(onto.Egg_Allergy))

        if request.form.get('wheat_allergy'):
            equiv = equiv & Not(onto.hasAllergy.some(onto.Wheat_Allergy))

        if request.form.get('tree_nut_allergy'):
            equiv = equiv & Not(onto.hasAllergy.some(onto.Tree_Nuts_Allergy))

        if request.form.get('peanut_allergy'):
            equiv = equiv & Not(onto.hasAllergy.some(onto.Peanut_Allergy))

        if request.form.get('crustacean_allergy'):
            equiv = equiv & Not(onto.hasAllergy.some(onto.Crustacean_shellfish_allergy))

        if request.form.get('soybeans_allergy'):
            equiv = equiv & Not(onto.hasAllergy.some(onto.Soybeans_Allergy))


        class MyClass(Thing):
            equivalent_to = [equiv]

        print(MyClass.equivalent_to)

        close_world(onto)
        sync_reasoner_pellet([onto])

        print(MyClass.equivalent_to)

        leaves = []
        for c in MyClass.equivalent_to[1:]:

            leaves.append(c)
        leaves += get_leaves(MyClass)
        rows = []

        response = {
            'foods': [str(f) for f in leaves],
            'form': request.form,
        }

    return render_template('index.html', data=response)


if __name__ == '__main__':
    app.run(debug=True, port=5005)