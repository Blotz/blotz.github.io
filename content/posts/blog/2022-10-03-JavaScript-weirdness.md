---
title: "JavaScript  Weirdness"
date: 2022-10-03T15:41:16+01:00
tags:
    - Software
category:
    - blog
keywords:
    - JavaScript
    - Compiler
comments: false
draft: true
---

JavaScript is strange.
It is a lawless wasteland of a language.

Many examples of its oddities come from a small feature known as "Type Coercion".
Type Coercion is usually how so many of those viral "javascript wtf" posts are made.

For example:

```javascript
> ('b'+'a'+ +'a'+'a').toLowerCase();
"banana"
> 2+"2"+2
222
> 2+"2"-2
20
> true + false
1
```

These are examples of JavaScript's type coercion at work.

## Type Coercion

What the hell is Type Coercion anyway?

Type Coercion is the process of converting one value from  one type to another.
This could be converting `"1"` to `1` when doing arithmetic or converting `0` to `false` when doing logical operations.
You can find an example of some of the Type Coercion, JavaScript will do at [this lovely site](https://dorey.github.io/JavaScript-Equality-Table/).

There are, in fact, two types of Type Coercion.
One that you are most likely familiar with and one that you probably hadn't noticed.
Implicit and Explicit Type Coercion.

Explicit Type Coercion is most likely the kind you are accustom to.
It happens when developers write code which *explicitly* converts one value to another.

Implicit Type Coercion happens in weakly typed languages.
It is when the value of a variable is converted to a different type, by the language, to allow the developer to perform operations on multiple types.
This can often have unforeseen results as Order of Operations can result in wtf evaluations.

For example in our "banana" example

```javascript
> ('b'+'a'+ +'a'+'a').toLowerCase();
"banana"
```

The Order of Operations looks roughly like this.

```javascript
> (('b'+'a'+ (+'a')+'a')).toLowerCase();
```

With JavaScript evaluating from the inner most bracket out.
Starting with `+'a'`, JavaScript assumes we are trying to perform arithmetic on the following value.
`'a'` is implicitly converted to a number though Type Coercion.
Due to the fact that `'a'` isn't a number, it results in `NaN`.

```javascript
> ('b'+'a'+ NaN +'a').toLowerCase();
```

Here, JavaScript performs another sneaky bit of Type Coercion and converts `NaN` into `'NaN'`.
Once done, it combines all of the strings together to `'baNaNa'` which is finally converted to lowercase and we get our "banana".

## Taking it to the extreme

Using Type Coercion, you can basically write any javascript with the following  symbols. `({[/>+!-=\]})`.
Furthermore, you can easily write a compiler which takes any valid JavaScript program and converts it to only use these 14 characters.

### Converting JavaScript

In order to write our compiler for JavaScript, we a91562a


#### Numbers

Numbers are simple enough to represent in our limited character set

If we do `true+0===1`, `true` is coerced into being `1`.
In Addition, we can do `!0===true` due to the fact that `!0` coerces `0` into being `false` which then evaluates to `true`.

```javascript
const zero = +[];
const one = +true;
```

however, as true isn't in our character set, we need to replace it with `!![]` so.

```javascript
const zero = +[];
const one = +!![];
```

If we want any other number, we can simply add our "one" to itself over and over till we reach the desired number.
This can be represented in a function

```javascript
const zero = '+[]';
const one = '+!![]';

const number = n => {
    if (n===0) return zero;
    return Array.from({length: n}, () => one).join(' + ');
}
```

#### Characters
