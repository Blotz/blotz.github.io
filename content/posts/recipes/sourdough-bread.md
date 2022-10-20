---
title: "Sourdough Bread"
date: 2022-10-20T20:08:35+01:00
category:
    - cooking
    - baking
keywords:
    - recipes
    - sourdough
    - bread
comments: true
draft: false
---
Sourdough is a fickle bread. The bread timings vary day to day depending on the environment you bake in and other conditions.
You shouldn't follow this recipe exactly and should do things based on what your heart desires.
Only then will you achieve a beautiful home-y loaf of bread.

## Sourdough Starter Care

Either store your Sourdough Starter on the counter or in your fridge.

If you store your sourdough in your fridge, it will be required to be feed once a week rather than every day.
If you forget to feed your sourdough for a while, don't panic.
Low temperatures in the fridge will cause your Starter to hibernate.
Simply scrape out some good sourdough and transfer to a bowel.
Then clean out your Starter Jar and return the Starter.
Then feed like usual. It should return to its bubbly self in at least 2 feeds

### Feeding

First you need to discard up to 90% of your Starter.
This is because Sourdough Starter grows much faster than we can bake it.

Then you need to mix in around 30g of flour and 30g of water in a 1 to 1 ratio.
This will result in a 100% hydration Starter.

Try to feed your Sourdough Starter at least 4-8 hours before you want to make your bread

## Equipment

### Basic Equipment

This is a basic list of equipment for baking sourdough.
Sourdough doesn't require fancy equipment and you can always try and make do without some of the equipment I list here.

- Mixing bowl
- Oven Tray
- A tightly woven tea towel*
- Kitchen Scissors or Sharp knife
- Spray bottle of water for misting

### Fancier Equipment

This is mainly what I use for my bread baking.
You don't need any of this to bake a beautiful bread but they make the process of bread baking easier.

- Mixing bowl
- Oven Tray
- Banneton Bread Proofing Basket
- Bread Lame
- Spray bottle of water for misting

## Ingredients

These will be rough amounts for a basic sourdough.
Feel free to experiment with ingredient amounts.
While I was learning how to make sourdough, I would play around with these amounts so that I could see what effect changing these ratios has on the loaf

For a basic sourdough loaf:

- 400g Bread Flour (100%)
- 280g Water (70%)
- 100g Sourdough Starter (25%)
- 8g Salt (2%)
- All-Purpose or Bread flour for dusting
- Rice Flour for bread basket*

(*This can also be swapped out for Plain White Flour)

If you are baking with a dutch oven, I recommend increasing the ratio of water to 75%.
As this recipe is for baking on a baking sheet, the 75% water results in a very fluid loaf doesn't bake well on an oven tray.

### Calculator

A simple calculator for calculating ingredient amounts for sizes of bread.

{{< rawhtml >}}
<form class="recipe_calculator" name="recipe_calculator" action="javascript:calculate_recipe()">
    <input name="amount" id="amount" type="number">
    <select name="ingredient" id="ingredient">
        <option value="flour">Bread Flour</option>
        <option value="water">Water</option>
        <option value="starter">Sourdough Starter</option>
    </select>
    <input type="button" onclick="calculate_recipe()" value="Submit">
</form>
<ul id="recipe_output"></ul>

<script>
    const FLOUR_PERCENTAGE=1
    const WATER_PERCENTAGE=0.70
    const STARTER_PERCENTAGE=0.25
    const SALT_PERCENTAGE=0.02

    function calculate_recipe() {
        var ingredient = document.recipe_calculator.ingredient.value
        var amount = document.recipe_calculator.amount.value
        if (amount=="") {
            return;
        }
        amount = parseInt(amount);
        var flour;
        var water;
        var starter;
        var salt;
        switch (ingredient) {
            case "flour":
                flour=amount;
                break;
            case "water":
                flour=amount/WATER_PERCENTAGE;
                break;
            case "starter":
                flour=amount/STARTER_PERCENTAGE;
                break;
            default:
                console.log("Error!");
                return;
        }
        water=flour*WATER_PERCENTAGE;
        starter=flour*STARTER_PERCENTAGE;
        salt=flour*SALT_PERCENTAGE;

        var output = document.getElementById("recipe_output");
        output.innerHTML = "";

        var li_flour = document.createElement("li");
        var li_water = document.createElement("li");
        var li_starter = document.createElement("li");
        var li_salt = document.createElement("li");

        li_flour.innerText = `${+flour.toFixed(2)}g Bread Flour`;
        li_water.innerText = `${+water.toFixed(2)}g Water`;
        li_starter.innerText = `${+starter.toFixed(2)}g Sourdough Starter`;
        li_salt.innerText = `${+salt.toFixed(2)}g Salt`;

        output.appendChild(li_flour);
        output.appendChild(li_water);
        output.appendChild(li_starter);
        output.appendChild(li_salt);
    }
</script>
<noscript>Sorry, your browser doesn't support JavaScript</noscript>
{{< /rawhtml >}}

## Instructions

This recipe is a slow recipe which will take at around three days to finish.

1. Sourdough Starter Prep.

    Take your sourdough starter out the fridge and place all of your discard in a air tight container.
    Add to the same container equal parts flour and water in proportion to the recipe.
    This allows you to prepare larger quantities of bread if you decide to batch cook several loafs at once.
2. Mix and First Proof.

    The next day, in a large mixing bowl, add Strong White Flour, Water, Sourdough Starter, and Salt.
    Blend these ingredients together in the large mixing bowl using your hands or a wooden spoon.

    Cover the bowl with a tea towel or tin foil and place in a warm place for 8-10 hours.
    This is the first proof.

    This process will help develop the Gluten in your loaf.
    Sourdough is considered a no knead bread as it doesn't require any intensive kneading.
3. Stretch and fold during Proof.

    After leaving the dough to rest/proof for 30 mins, you want to stretch and fold the dough onto itself with wet hands.
    Repeat this action several times while rotating the bowl to fully stretch and fold.
    Then repeat this every 1-2 hours till the dough is smooth and workable.

    The action of stretching and folding helps develop gluten in the bread which results in a lighter, fluffier loaf.

4. Forming the dough and Second Proof.

    Scrape your bread dough onto a lightly floured surface. Shape the dough into a smooth ball with an unbroken surface.
    I do this by pushing dough, from the sides, down and into the bottom of the ball.
    Then pinching it together until the dough is smooth.

    Generously dust your loaf with rice flour.
    Place the bread, smooth side down, into the banneton*.
    Then cover the banneton* with a tea towel or tin foil and place inside of the fridge for 12 to 18 hours to retard

    retard is the process of slowing down the final proof which allows it's flavour to develop and gives us more time to bake.

    (*You can use a similarly sized bowl + a tightly woven tea-towel as a substitution or simply wrap the bread in a clean tightly woven tea-towel)

5. Bake!

    Preheat the oven to 230C(450F) fan and line a baking sheet with parchment paper.

    Gently invert your banneton over your baking sheet and transfer the dough to the tray.
    Brush off excess rice flour and score the top of your dough with your bread lame or sharp knife.

    Thoroughly Spritz your bread/oven with water as you place it inside the oven.
    This is to create a humid environment for the bread to bake which promotes caramelization in the crust.

6. Leave To cool

    Take loaf out and leave to cool. (Do not slice loaf while still warm)
