# rCore 实验

## 🔗相关链接

2022年开源操作系统训练营：https://github.com/LearningOS/rust-based-os-comp2022/blob/main/scheduling.md

项目官网：https://os2edu.cn/homepage/

实验视频地址：https://cloud.tsinghua.edu.cn/d/ce9eced17e89471c8c30/

资源汇总：https://github.com/chyyuu/os_course_info

2021 项目学习路径：https://github.com/rcore-os/rCore/wiki/os-tutorial-summer-of-code-2021

Rust 学习资料汇总：https://github.com/rust-boom/rust-boom

## Rust 环境配置与使用

### 安装 Rust

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### 用 cargo 创建新项目

```bash
cargo new hello_cargo
```

### cargo 编译

```bash
cargo build
```

### cargo 编译并运行

```bash
cargo run
```

快速检查代码确保其可以编译，并不产生可执行文件

```
cargo check
```

## Rustlings

排行榜：https://os2edu.cn/ranking/rank

零基础 Rust 学习文档：https://kaisery.github.io/trpl-zh-cn/title-page.html

零基础 Rust 学习文档可以结合视频看：https://www.bilibili.com/video/BV1hp4y1k7SV

Rust 语法查询文档，Rust by example，合适有基础的人看：https://rustwiki.org/zh-CN/rust-by-example/index.html

Rust 标准库文档：https://doc.rust-lang.org/std/index.html

rustlings 答案分享：https://github.com/master-davidlee/rustlings_answer/tree/master/exercises%20v0.4

### 安装使用

```bash
curl -L https://raw.githubusercontent.com/rust-lang/rustlings/main/install.sh | bash
```

运行

```bash
cd rustlings/
```

按给定的练习顺序自动编译完成的练习，编译不通过给出报错

```bash
rustlings watch
```

- 删掉注释 // I AM NOT DONE 即可自动编译。 

查看当前练习完成情况

```bash
rustlings list
```

下面是题解

### 1. intro/intro1.rs

删掉 // I AM NOT DONE，编译通过。

### 2. intro/intro2.rs

占位符缺少参数，修改为

```diff
- println!("Hello {}!");
+ println!("Hello {}!", 1);
```

通过编译。

### 3. variables/variables1.rs

使用 `let` 语句来创建变量，修改为

```diff
fn main() {
-    x = 5;
+    let x = 5;
    println!("x has the value {}", x);
}
```

### 4. variables/variables2.rs

let 作用是创建变量并赋值，不能只创建变量不赋值，修改为

```diff
fn main() {
-    let x;
+    let x = 5;
    if x == 10 {
        println!("x is ten!");
    } else {
        println!("x is not ten!");
    }
}
```

### 5. variables/variables3.rs

创建变量时不能只指定变量类型，还要初始化。

```diff
fn main() {
-    let x: i32;
+    let x: i32 = 5;
    println!("Number {}", x);
}
```

### 6. variables/variables4.rs

Rust 变量默认是不可变变量，需要加上 mut 才可以改变数值。

如果一部分代码假设一个值永远也不会改变，而另一部分代码改变了这个值，第一部分代码就有可能以不可预料的方式运行。

```diff
fn main() {
-    let x = 3;
+    let mut x = 3;
    println!("Number {}", x);
    x = 5; // don't change this line
    println!("Number {}", x);
}
```

### 7. variables/variables5.rs

Rust 允许用一个新值来 **隐藏** （*shadow*） `number` 之前的值。这个功能常用在需要转换值类型之类的场景。它允许我们复用 `number` 变量的名字，而不是被迫创建两个不同变量。

```diff
fn main() {
    let number = "T-H-R-E-E"; // don't change this line
    println!("Spell a Number : {}", number);
-    number = 3; // don't rename this variable
+    let number = 3; // don't rename this variable
    println!("Number plus two is : {}", number + 2);
}
```

### 8. variables/variables6.rs

常量不光默认不能变，它总是不能变。声明常量使用 `const` 关键字而不是 `let`，并且必须注明值的类型。

```diff
- const NUMBER = 3;
+ const NUMBER: i32 = 3;
fn main() {
    println!("Number {}", NUMBER);
}
```

### 9. functions/functions1.rs

`fn` 关键字用来声明新函数，Rust 不关心函数定义所在的位置，只要函数被调用时出现在调用之处可见的作用域内就行。

```diff
fn main() {
    call_me();
}

+ fn call_me(){}
```

### 10. functions/functions2.rs

在函数签名中，**必须** 声明每个参数的类型。这是 Rust 设计中一个经过慎重考虑的决定：要求在函数定义中提供类型注解，意味着编译器再也不需要你在代码的其他地方注明类型来指出你的意图。而且，在知道函数需要什么类型后，编译器就能够给出更有用的错误消息。

```diff
fn main() {
    call_me(3);
}

- fn call_me(num:) {
+ fn call_me(num: i32) {
    for i in 0..num {
        println!("Ring! Call number {}", i + 1);
    }
}
```

### 11. functions/functions3.rs

函数传参需要参数

```diff
fn main() {
-    call_me();
+    call_me(3);
}

fn call_me(num: u32) {
    for i in 0..num {
        println!("Ring! Call number {}", i + 1);
    }
}
```

### 12. functions/functions4.rs

Rust 并不对返回值命名，但要在箭头（`->`）后声明它的类型。在 Rust 中，函数的返回值等同于函数体最后一个表达式的值。

```diff
fn main() {
    let original_price = 51;
    println!("Your sale price is {}", sale_price(original_price));
}
- fn sale_price(price: i32) -> {
+ fn sale_price(price: i32) -> i32 {
    if is_even(price) {
        price - 10
    } else {
        price - 3
    }
}

fn is_even(num: i32) -> bool {
    num % 2 == 0
}
```

### 13. functions/functions5.rs

表达式的结尾没有分号。如果在表达式的结尾加上分号，它就变成了语句，而语句不会返回值。

```diff
fn main() {
    let answer = square(3);
    println!("The square of 3 is {}", answer);
}

fn square(num: i32) -> i32 {
-    num * num;
+    num * num
}
```

### 14. if/if1.rs

依照手册，编写控制流，注意表达式不加分号才有返回值。

```diff
pub fn bigger(a: i32, b: i32) -> i32 {
    // Complete this function to return the bigger number!
    // Do not use:
    // - another function call
    // - additional variables
+    if a < b {
+        b
+    } else {
+        a
+    }
}

// Don't mind this for now :)
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ten_is_bigger_than_eight() {
        assert_eq!(10, bigger(10, 8));
    }

    #[test]
    fn fortytwo_is_bigger_than_thirtytwo() {
        assert_eq!(42, bigger(32, 42));
    }
}
```

### 15. if/if2.rs

利用多分支重新编写 foo_if_fizz 函数

```rust
pub fn foo_if_fizz(fizzish: &str) -> &str {
    if fizzish == "fizz" {
        "foo"
    } else if fizzish == "fuzz"{
        "bar"
    } else {
        "baz"
    }
}
```

### 16. quiz1.rs

编写 calculate_price_of_apples 函数

```rust
fn calculate_price_of_apples(num: i32) -> i32 {
    if num <= 40 {
        2 * num
    } else {
        num
    }
}
```

### 17. primitive_types/primitive_types1.rs

```diff
fn main() {
    // Booleans (`bool`)

    let is_morning = true;
    if is_morning {
        println!("Good morning!");
    }

+    let is_evening = false; // Finish the rest of this line like the example! Or make it be false!
    if is_evening {
        println!("Good evening!");
    }
}
```

### 18. primitive_types/primitive_types2.rs

仿写，定义一个变量，初始化为一个字母。

```rust
let your_character = 'B'; // Finish this line like the example! What's your favorite character?
```

### 19. primitive_types/primitive_types3.rs

初始化变量 a 为 0。

```diff
fn main() {
+    let a = [0i32;100];

    if a.len() >= 100 {
        println!("Wow, that's a big array!");
    } else {
        println!("Meh, I eat arrays like that for breakfast.");
    }
}
```

### 20. primitive_types/primitive_types4.rs

利用 Rust 切片。slice 允许你引用集合中一段连续的元素序列，而不用引用整个集合。slice 是一类引用，所以它没有所有权。

```diff
#[test]
fn slice_out_of_array() {
    let a = [1, 2, 3, 4, 5];

+    let nice_slice = &a[1..4];

    assert_eq!([2, 3, 4], nice_slice)
}
```

### 21. primitive_types/primitive_types5.rs

```diff
fn main() {
    let cat = ("Furry McFurson", 3.5);
+    let (name, age) = cat;

    println!("{} is {} years old.", name, age);
}
```

### 22. primitive_types/primitive_types6.rs

元组的索引是用点号访问的。

```diff
#[test]
fn indexing_tuple() {
    let numbers = (1, 2, 3);
    // Replace below ??? with the tuple indexing syntax.
+    let second = numbers.1;

    assert_eq!(2, second,
        "This is not the 2nd number in the tuple!")
}
```

### 23. vecs/vecs1.rs

Rust 提供了 `vec!` 宏，这个宏会根据我们提供的值来创建一个新的 vector。

```rust
let v = vec![10, 20, 30, 40];
```

或者使用 to_vec()，克隆整个切片，返回一个新的向量，使用 v[..] 就可以把向量变成数组。

```rust
let v = [10, 20, 30, 40].to_vec();
```

### 24. vecs/vecs2.rs

利用解引用运算符追踪指针的值，修改可变引用所指向的值。

```diff
fn vec_loop(mut v: Vec<i32>) -> Vec<i32> {
    for i in v.iter_mut() {
        // TODO: Fill this up so that each element in the Vec `v` is
        // multiplied by 2.
+        *i *= 2;
    }

    // At this point, `v` should be equal to [4, 8, 12, 16, 20].
    v
}

fn vec_map(v: &Vec<i32>) -> Vec<i32> {
    v.iter().map(|num| {
        // TODO: Do the same thing as above - but instead of mutating the
        // Vec, you can just return the new number!
+        num * 2
    }).collect()
}
```

### 25. move_semantics/move_semantics1.rs

修改 vec1，需要让 vec1 变成可变变量。

```diff
fn main() {
    let vec0 = Vec::new();

+    let mut vec1 = fill_vec(vec0);

    println!("{} has length {} content `{:?}`", "vec1", vec1.len(), vec1);

    vec1.push(88);

    println!("{} has length {} content `{:?}`", "vec1", vec1.len(), vec1);
}
```

### 26. move_semantics/move_semantics2.rs

对 vec0 进行修改需要将 vec0 变为可变变量。

```diff
fn main() {
-    let vec0 = Vec::new();
+    let mut vec0 = Vec::new();

-    let mut vec1 = fill_vec(vec0);
+    let mut vec1 = fill_vec(&mut vec0);

    // Do not change the following line!
    println!("{} has length {} content `{:?}`", "vec0", vec0.len(), vec0);

    vec1.push(88);

    println!("{} has length {} content `{:?}`", "vec1", vec1.len(), vec1);
}

- fn fill_vec(vec: Vec<i32>) -> Vec<i32> {
+ fn fill_vec(vec: &mut Vec<i32>) -> Vec<i32> {
    let mut vec = vec;

    vec.push(22);
    vec.push(44);
    vec.push(66);

-    vec
+    vec.to_vec()
}
```

### 27. move_semantics/move_semantics3.rs

与 26 题类似。

```diff
fn main() {
-    let vec0 = Vec::new();
+    let mut vec0 = Vec::new();

-    let mut vec1 = fill_vec(vec0);
+    let mut vec1 = fill_vec(&mut vec0);

    println!("{} has length {} content `{:?}`", "vec1", vec1.len(), vec1);

    vec1.push(88);

    println!("{} has length {} content `{:?}`", "vec1", vec1.len(), vec1);
}

- fn fill_vec(vec: Vec<i32>) -> Vec<i32> {
+ fn fill_vec(vec: &mut Vec<i32>) -> Vec<i32> {
    vec.push(22);
    vec.push(44);
    vec.push(66);

-    vec
+    vec.to_vec()
}
```

### 28. move_semantics/move_semantics4.rs

```diff
fn main() {
-    let vec0 = Vec::new();

-    let mut vec1 = fill_vec(vec0);
+    let mut vec1 = fill_vec();

    println!("{} has length {} content `{:?}`", "vec1", vec1.len(), vec1);

    vec1.push(88);

    println!("{} has length {} content `{:?}`", "vec1", vec1.len(), vec1);
}

// `fill_vec()` no longer takes `vec: Vec<i32>` as argument
fn fill_vec() -> Vec<i32> {
-    let mut vec = vec;
+    let mut vec = vec![];

    vec.push(22);
    vec.push(44);
    vec.push(66);

    vec
}
```

### 29. move_semantics/move_semantics5.rs

因为我们不能在同一时间多次将 `x` 作为可变变量借用。防止同一时间对同一数据存在多个可变引用。这个限制的好处是 Rust 可以在编译时就避免数据竞争。可以使用大括号来创建一个新的作用域，以允许拥有多个可变引用，只是不能 **同时** 拥有

```diff
fn main() {
    let mut x = 100;
+    {
        let y = &mut x;
        *y += 100;
+    }
    let z = &mut x;
    *z += 1000;
    assert_eq!(x, 1200);
}
```

### 30. move_semantics/move_semantics6.rs

变量传递到函数里面，所有权就给了函数，函数结束，变量就被释放了，所以不能再用 data 变量。可以一开始先引用，不获取所有权，这样第二次就可以用了。

```diff
fn main() {
    let data = "Rust is great!".to_string();

-    get_char(data);
+    get_char(&data);

-    string_uppercase(&data);
+    string_uppercase(data);
}

// Should not take ownership
- fn get_char(data: String) -> char {
+ fn get_char(data: &String) -> char {
    data.chars().last().unwrap()
}

// Should take ownership
- fn string_uppercase(mut data: &String) {
+ fn string_uppercase(mut data: String) {
-    data = &data.to_uppercase();
+    data = data.to_uppercase();

    println!("{}", data);
}
```

### 31. structs/structs1.rs

```diff
struct ColorClassicStruct {
+    red: i32,
+    green: i32,
+    blue: i32,
    // TODO: Something goes here
}

struct ColorTupleStruct(i32, i32, i32);

#[derive(Debug)]
struct UnitLikeStruct;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn classic_c_structs() {
        // TODO: Instantiate a classic c struct!
+        let green = ColorClassicStruct {
+            red: 0,
+            green: 255,
+            blue: 0,
+        };

        assert_eq!(green.red, 0);
        assert_eq!(green.green, 255);
        assert_eq!(green.blue, 0);
    }

    #[test]
    fn tuple_structs() {
        // TODO: Instantiate a tuple struct!
+        let green = ColorTupleStruct(0, 255, 0);

        assert_eq!(green.0, 0);
        assert_eq!(green.1, 255);
        assert_eq!(green.2, 0);
    }

    #[test]
    fn unit_structs() {
        // TODO: Instantiate a unit-like struct!
+        let unit_like_struct = UnitLikeStruct;
        let message = format!("{:?}s are fun!", unit_like_struct);

        assert_eq!(message, "UnitLikeStructs are fun!");
    }
}
```

### 32. structs/structs2.rs

```diff
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn your_order() {
        let order_template = create_order_template();
        // TODO: Create your own order using the update syntax and template above!
+        let your_order = Order {
+            name: String::from("Hacker in Rust"),
+            year: 2019,
+            made_by_phone: false,
+            made_by_mobile: false,
+            made_by_email: true,
+            item_number: 123,
+            count: 1,
+        };
        assert_eq!(your_order.name, "Hacker in Rust");
        assert_eq!(your_order.year, order_template.year);
        assert_eq!(your_order.made_by_phone, order_template.made_by_phone);
        assert_eq!(your_order.made_by_mobile, order_template.made_by_mobile);
        assert_eq!(your_order.made_by_email, order_template.made_by_email);
        assert_eq!(your_order.item_number, order_template.item_number);
        assert_eq!(your_order.count, 1);
    }
}
```

### 33. structs/structs3.rs

根据题意，补全代码

```diff
impl Package {
    fn new(sender_country: String, recipient_country: String, weight_in_grams: i32) -> Package {
        if weight_in_grams <= 0 {
            panic!("Can not ship a weightless package.")
        } else {
            Package {
                sender_country,
                recipient_country,
                weight_in_grams,
            }
        }
    }

+    fn is_international(&self) -> bool {
        // Something goes here...
+        self.sender_country != self.recipient_country
    }

+    fn get_fees(&self, cents_per_gram: i32) -> i32 {
        // Something goes here...
+        cents_per_gram * self.weight_in_grams
    }
}
```

### 34. enums/enums1.rs

补全枚举对象

```diff
#[derive(Debug)]
enum Message {
    // TODO: define a few types of messages as used below
+    Quit,
+    Echo,
+    Move,
+    ChangeColor,
}

fn main() {
    println!("{:?}", Message::Quit);
    println!("{:?}", Message::Echo);
    println!("{:?}", Message::Move);
    println!("{:?}", Message::ChangeColor);
}
```

### 35. enums/enums2.rs

补全枚举对象

```diff
#[derive(Debug)]
enum Message {
    // TODO: define the different variants used below
+    Move {x: i32, y: i32},
+    Echo(String),
+    ChangeColor(i32, i32, i32),
+    Quit,
}
```

### 36. enums/enums3.rs

使用 match 匹配参数。

```diff
enum Message {
    // TODO: implement the message variant types based on their usage below
+    ChangeColor((u8, u8, u8)),
+    Echo(String),
+    Move(Point),
+    Quit,
}

struct Point {
    x: u8,
    y: u8,
}

struct State {
    color: (u8, u8, u8),
    position: Point,
    quit: bool,
}

impl State {
    fn change_color(&mut self, color: (u8, u8, u8)) {
        self.color = color;
    }

    fn quit(&mut self) {
        self.quit = true;
    }

    fn echo(&self, s: String) {
        println!("{}", s);
    }

    fn move_position(&mut self, p: Point) {
        self.position = p;
    }

    fn process(&mut self, message: Message) {
        // TODO: create a match expression to process the different message variants
+        match message {
+            Message::ChangeColor(a) => self.change_color(a),
+            Message::Echo(b) => self.echo(b),
+            Message::Move(c) => self.move_position(c),
+            Message::Quit => self.quit(),
+        }
    }
}
```

### 37. strings/strings1.rs

根据报错提示。

```diff
fn main() {
    let answer = current_favorite_color();
    println!("My current favorite color is {}", answer);
}

fn current_favorite_color() -> String {
-    "blue"
+    "blue".to_string()
}
```

### 38. strings/strings2.rs

```diff
fn main() {
    let word = String::from("green"); // Try not changing this line :)
-    if is_a_color_word(word) {
+    if is_a_color_word(&word) {
        println!("That is a color word I know!");
    } else {
        println!("That is not a color word I know.");
    }
}
```

### 39. strings/strings3.rs

- `to_owned()` 从一个字符串切片中创建一个具有所有权的 `String`

```diff
fn trim_me(input: &str) -> String {
    // TODO: Remove whitespace from both ends of a string!
+    input.trim().to_string()
}

fn compose_me(input: &str) -> String {
    // TODO: Add " world!" to the string! There's multiple ways to do this!
+    input.to_owned() + " world!"
}

fn replace_me(input: &str) -> String {
    // TODO: Replace "cars" in the string with "balloons"!
+    input.replace("cars", "balloons")
}
```

### 40. strings/strings4.rs

- "blue" 单纯的字符串是 &str 类型。

- format! 由于 fmt::Display trait，它会自动提供 ToString。

```diff
fn string_slice(arg: &str) {
    println!("{}", arg);
}
fn string(arg: String) {
    println!("{}", arg);
}

fn main() {
+    string_slice("blue");
+    string("red".to_string());
+    string(String::from("hi"));
+    string("rust is fun!".to_owned());
+    string("nice weather".into());
+    string(format!("Interpolation {}", "Station"));
+    string_slice(&String::from("abc")[0..1]);
+    string_slice("  hello there ".trim());
+    string("Happy Monday!".to_string().replace("Mon", "Tues"));
+    string("mY sHiFt KeY iS sTiCkY".to_lowercase());
}
```

### 41. modules/modules1.rs

将 **make_sausage** 暴露，外部函数才可以访问。

```diff
mod sausage_factory {
    // Don't let anybody outside of this module see this!
    fn get_secret_recipe() -> String {
        String::from("Ginger")
    }
-    fn make_sausage() {
+    pub fn make_sausage() {
        get_secret_recipe();
        println!("sausage!");
    }
}

fn main() {
    sausage_factory::make_sausage();
}
```

### 42. modules/modules2.rs

使用 pub use

```diff
mod delicious_snacks {
    // TODO: Fix these use statements
+    pub use self::fruits::PEAR as fruit;
+    pub use self::veggies::CUCUMBER as veggie;

    mod fruits {
        pub const PEAR: &'static str = "Pear";
        pub const APPLE: &'static str = "Apple";
    }

    mod veggies {
        pub const CUCUMBER: &'static str = "Cucumber";
        pub const CARROT: &'static str = "Carrot";
    }
}

fn main() {
    println!(
        "favorite snacks: {} and {}",
        delicious_snacks::fruit,
        delicious_snacks::veggie
    );
}
```

### 43. modules/modules3.rs

引入标准库

```diff
+ use std::time::*;

fn main() {
    match SystemTime::now().duration_since(UNIX_EPOCH) {
        Ok(n) => println!("1970-01-01 00:00:00 UTC was {} seconds ago!", n.as_secs()),
        Err(_) => panic!("SystemTime before UNIX EPOCH!"),
    }
}
```

### 44. hashmaps/hashmaps1.rs

按要求增加水果。

```diff
use std::collections::HashMap;

fn fruit_basket() -> HashMap<String, u32> {
+    let mut basket = HashMap::new(); // TODO: declare your hash map here.

    // Two bananas are already given for you :)
    basket.insert(String::from("banana"), 2);
    
    // TODO: Put more fruits in your basket here.
+    basket.insert(String::from("apple"), 2);
+    basket.insert(String::from("pear"), 1);

    basket
}
```

### 45. hashmaps/hashmaps2.rs

当水果不存在时加入键值对。

```diff
fn fruit_basket(basket: &mut HashMap<Fruit, u32>) {
    let fruit_kinds = vec![
        Fruit::Apple,
        Fruit::Banana,
        Fruit::Mango,
        Fruit::Lychee,
        Fruit::Pineapple,
    ];

    for fruit in fruit_kinds {
        // TODO: Put new fruits if not already present. Note that you
        // are not allowed to put any type of fruit that's already
        // present!
+        basket.entry(fruit).or_insert(5);
    }
}
```

### 46. hashmaps/hashmaps3.rs

用函数构建结构体，目前还不会复制所有权，代码比较复杂，以后再修改。

```rust
struct Team {
    name: String,
    goals_scored: u8,
    goals_conceded: u8,
}

fn build_Team(name: String, goals_scored: u8, goals_conceded: u8) -> Team {
    Team {
        name,
        goals_scored,
        goals_conceded,
    }
}

fn build_scores_table(results: String) -> HashMap<String, Team> {
    // The name of the team is the key and its associated struct is the value.
    let mut scores: HashMap<String, Team> = HashMap::new();

    for r in results.lines() {
        let v: Vec<&str> = r.split(',').collect();
        // TODO: Populate the scores table with details extracted from the
        // current line. Keep in mind that goals scored by team_1
        // will be number of goals conceded from team_2, and similarly
        // goals scored by team_2 will be the number of goals conceded by
        // team_1.
        let team1 = build_Team (
            v[0].to_string(),
            v[2].parse().unwrap(),
            v[3].parse().unwrap(),
        );
        let team11 = build_Team (
            v[0].to_string(),
            0,
            0,
        );
        let team111 = build_Team (
            v[0].to_string(),
            v[2].parse().unwrap(),
            v[3].parse().unwrap(),
        );
        let team2 = build_Team (
            v[1].to_string(),
            v[3].parse().unwrap(),
            v[2].parse().unwrap(),
        );
        let team22 = build_Team (
            v[1].to_string(),
            0,
            0,
        );
        let team222 = build_Team (
            v[1].to_string(),
            v[3].parse().unwrap(),
            v[2].parse().unwrap(),
        );
        let count1 = scores.entry(team1.name).or_insert(team11);
        (*count1).goals_scored += team111.goals_scored;
        (*count1).goals_conceded += team111.goals_conceded;
        let count2 = scores.entry(team2.name).or_insert(team22);
        (*count2).goals_scored += team222.goals_scored;
        (*count2).goals_conceded += team222.goals_conceded;
    }
    scores
}
```

### 47. quiz2.rs

利用 match 匹配模式。

```rust
pub enum Command {
    Uppercase,
    Trim,
    Append(usize),
}

mod my_module {
    use super::Command;

    // TODO: Complete the function signature!
    pub fn transformer(input: Vec<(String, Command)>) -> Vec<String> {
        // TODO: Complete the output declaration!
        let mut output: Vec<String> = vec![];
        for (index, (string, command)) in input.iter().enumerate() {
            // TODO: Complete the function body. You can do it!
            output.push(string.to_string());
            match command {
                Command::Uppercase => output[index] = output[index].to_uppercase(),
                Command::Trim => output[index] = output[index].trim().to_string(),
                Command::Append(size) => {
                    for i in 1..=*size {
                        output[index].push_str("bar");
                    }
                },
            }
        }
        output
    }
}

#[cfg(test)]
mod tests {
    // TODO: What do we have to import to have `transformer` in scope?
    use super::my_module::transformer;
    use super::Command;

    #[test]
    fn it_works() {
        let output = transformer(vec![
            ("hello".into(), Command::Uppercase),
            (" all roads lead to rome! ".into(), Command::Trim),
            ("foo".into(), Command::Append(1)),
            ("bar".into(), Command::Append(5)),
        ]);
        assert_eq!(output[0], "HELLO");
        assert_eq!(output[1], "all roads lead to rome!");
        assert_eq!(output[2], "foobar");
        assert_eq!(output[3], "barbarbarbarbarbar");
    }
}
```

### 48. options/options1.rs

利用[`Option` 枚举](https://kaisery.github.io/trpl-zh-cn/ch06-01-defining-an-enum.html#option-枚举和其相对于空值的优势)的特性编写代码。

```diff
fn maybe_icecream(time_of_day: u16) -> Option<u16> {
    // We use the 24-hour system here, so 10PM is a value of 22 and 12AM is a value of 0
    // The Option output should gracefully handle cases where time_of_day > 23.
+    if time_of_day < 22 {
+        Some(5)
+    } else if time_of_day <= 23 {
+        Some(0)
+    } else {
+        None
+    }
}
```

### 49. options/options2.rs

参考 https://rustwiki.org/zh-CN/rust-by-example/flow_control/while_let.html 写。

```diff
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn simple_option() {
        let target = "rustlings";
        let optional_target = Some(target);

        // TODO: Make this an if let statement whose value is "Some" type
+        if let Some(word) = optional_target {
            assert_eq!(word, target);
        }
    }

    #[test]
    fn layered_option() {
        let mut range = 10;
        let mut optional_integers: Vec<Option<i8>> = Vec::new();
        for i in 0..(range + 1) {
            optional_integers.push(Some(i));
        }

        // TODO: make this a while let statement - remember that vector.pop also adds another layer of Option<T>
        // You can stack `Option<T>`'s into while let and if let
+        while let Some(integer) = optional_integers.pop() {
+            assert_eq!(integer, Some(range));
            range -= 1;
        }
    }
}
```

### 50. options/options3.rs

编译报错，根据终端报错提示需要添加 ref。

```diff
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let y: Option<Point> = Some(Point { x: 100, y: 200 });

    match y {
+        Some(ref p) => println!("Co-ordinates are {},{} ", p.x, p.y),
        _ => println!("no match"),
    }
    y; // Fix without deleting this line.
}
```

### 51. error_handling/errors1.rs

将返回值改为 Result<String, String>。

```diff
+ pub fn generate_nametag_text(name: String) -> Result<String, String> {
    if name.is_empty() {
        // Empty names aren't allowed.
+        Err("`name` was empty; it must be nonempty.".into())
    } else {
+        Ok(format!("Hi! My name is {}", name))
    }
}
```

### 52. error_handling/errors2.rs

最简单的方法就是最后加一个问号。

```diff
pub fn total_cost(item_quantity: &str) -> Result<i32, ParseIntError> {
    let processing_fee = 1;
    let cost_per_item = 5;
+    let qty = item_quantity.parse::<i32>()?;

    Ok(qty * cost_per_item + processing_fee)
}
```

复杂一点的方法

```diff
pub fn total_cost(item_quantity: &str) -> Result<i32, ParseIntError> {
    let processing_fee = 1;
    let cost_per_item = 5;
+    let qty = match item_quantity.parse::<i32>() {
+        Ok(s) => Ok(s * cost_per_item + processing_fee),
+        Err(e) => Err(e),
+    };
+    qty
}
```

### 53. error_handling/errors3.rs

参考链接：[哪里可以使用 `?` 运算符](https://kaisery.github.io/trpl-zh-cn/ch09-02-recoverable-errors-with-result.html#哪里可以使用--运算符)

```diff
use std::num::ParseIntError;
+ use std::error::Error;

+ fn main() -> Result<(), Box<dyn Error>> {
    let mut tokens = 100;
    let pretend_user_input = "8";

    let cost = total_cost(pretend_user_input)?;

    if cost > tokens {
        println!("You can't afford that many!");
    } else {
        tokens -= cost;
        println!("You now have {} tokens.", tokens);
    }
+    Ok(())
}

pub fn total_cost(item_quantity: &str) -> Result<i32, ParseIntError> {
    let processing_fee = 1;
    let cost_per_item = 5;
    let qty = item_quantity.parse::<i32>()?;

    Ok(qty * cost_per_item + processing_fee)
}
```

### 54. error_handling/errors4.rs

不同情况不同错误处理。

```diff
impl PositiveNonzeroInteger {
    fn new(value: i64) -> Result<PositiveNonzeroInteger, CreationError> {
        // Hmm...? Why is this only returning an Ok value?
+        if value < 0 {
+            Err(CreationError::Negative)
+        } else if value == 0 {
+            Err(CreationError::Zero)
+        } else {
+            Ok(PositiveNonzeroInteger(value as u64))
+        }
    }
}
```

后面看到下一题有这一题的正解

```diff
impl PositiveNonzeroInteger {
    fn new(value: i64) -> Result<PositiveNonzeroInteger, CreationError> {
+        match value {
+            x if x < 0 => Err(CreationError::Negative),
+            x if x == 0 => Err(CreationError::Zero),
+            x => Ok(PositiveNonzeroInteger(x as u64))
+        }
    }
}
```

### 55. error_handling/errors5.rs

按照第 53 题的经验修改

```diff
use std::error;
use std::fmt;
use std::num::ParseIntError;
+ use error::Error;

// TODO: update the return type of `main()` to make this compile.
+ fn main() -> Result<(), Box<dyn Error>> {
    let pretend_user_input = "42";
    let x: i64 = pretend_user_input.parse()?;
    println!("output={:?}", PositiveNonzeroInteger::new(x)?);
    Ok(())
}
```

### 56. error_handling/errors6.rs

删掉 .unwrap()。参考：https://github.com/master-davidlee/rustlings_answer/blob/master/exercises%20v0.4/error_handling/errors6.rs

```diff
impl ParsePosNonzeroError {
    fn from_creation(err: CreationError) -> ParsePosNonzeroError {
        ParsePosNonzeroError::Creation(err)
    }
    // TODO: add another error conversion function here.
    // fn from_parseint...
+    fn from_parseint(err: ParseIntError) -> ParsePosNonzeroError {
+        ParsePosNonzeroError::ParseInt(err)
+    }
}

fn parse_pos_nonzero(s: &str)
    -> Result<PositiveNonzeroInteger, ParsePosNonzeroError>
{
    // TODO: change this to return an appropriate error instead of panicking
    // when `parse()` returns an error.
+    let x: i64 = s.parse().map_err(ParsePosNonzeroError::from_parseint)?;
    PositiveNonzeroInteger::new(x)
        .map_err(ParsePosNonzeroError::from_creation)
}
```

### 57. generics/generics1.rs

```diff
fn main() {
+    let mut shopping_list: Vec<&str> = Vec::new();
    shopping_list.push("milk");
}
```

### 58. generics/generics2.rs

根据泛型的文档填写：

```diff
+ struct Wrapper<T> {
+     value: T,
}

+ impl<T> Wrapper<T> {
+    pub fn new(value: T) -> Self {
        Wrapper { value }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn store_u32_in_wrapper() {
        assert_eq!(Wrapper::new(42).value, 42);
    }

    #[test]
    fn store_str_in_wrapper() {
        assert_eq!(Wrapper::new("Foo").value, "Foo");
    }
}
```

### 59. traits/traits1.rs

`format!` 和 `print!` 类似，但返回的是一个堆分配的字符串，而不是打印结果到控制台上。常用于连接字符串。

```diff
trait AppendBar {
    fn append_bar(self) -> Self;
}

impl AppendBar for String {
    //Add your code here
+    fn append_bar(self) -> Self {
+        format!("{}Bar", self)
+    }
}

fn main() {
    let s = String::from("Foo");
    let s = s.append_bar();
    println!("s: {}", s);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn is_foo_bar() {
        assert_eq!(String::from("Foo").append_bar(), String::from("FooBar"));
    }

    #[test]
    fn is_bar_bar() {
        assert_eq!(
            String::from("").append_bar().append_bar(),
            String::from("BarBar")
        );
    }
}
```

### 60. traits/traits2.rs

self 是不可变变量，需要克隆一个可变变量再返回。

```diff
trait AppendBar {
    fn append_bar(self) -> Self;
}

//TODO: Add your code here

+impl AppendBar for Vec<String> {
+    //Add your code here
+    fn append_bar(self) -> Self {
+        let mut vector = self.clone();
+        vector.push("Bar".to_string());
+        vector
+    }
+}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn is_vec_pop_eq_bar() {
        let mut foo = vec![String::from("Foo")].append_bar();
        assert_eq!(foo.pop().unwrap(), String::from("Bar"));
        assert_eq!(foo.pop().unwrap(), String::from("Foo"));
    }
}
```

### 61. traits/traits3.rs

为 trait 中的某些方法提供默认的行为

```diff
pub trait Licensed {
+    fn licensing_info(&self) -> String {
+        String::from("Some information")
+    }
}

struct SomeSoftware {
    version_number: i32,
}

struct OtherSoftware {
    version_number: String,
}

impl Licensed for SomeSoftware {} // Don't edit this line
impl Licensed for OtherSoftware {} // Don't edit this line

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn is_licensing_info_the_same() {
        let licensing_info = String::from("Some information");
        let some_software = SomeSoftware { version_number: 1 };
        let other_software = OtherSoftware {
            version_number: "v2.0.0".to_string(),
        };
        assert_eq!(some_software.licensing_info(), licensing_info);
        assert_eq!(other_software.licensing_info(), licensing_info);
    }
}
```

### 62. traits/traits4.rs

参考 [trait 作为参数](https://kaisery.github.io/trpl-zh-cn/ch10-02-traits.html#trait-作为参数) 一节实现

```diff
pub trait Licensed {
    fn licensing_info(&self) -> String {
        "some information".to_string()
    }
}

struct SomeSoftware {}

struct OtherSoftware {}

impl Licensed for SomeSoftware {}
impl Licensed for OtherSoftware {}

// YOU MAY ONLY CHANGE THE NEXT LINE
+ fn compare_license_types(software: impl Licensed, software_two: impl Licensed) -> bool {
    software.licensing_info() == software_two.licensing_info()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn compare_license_information() {
        let some_software = SomeSoftware {};
        let other_software = OtherSoftware {};

        assert!(compare_license_types(some_software, other_software));
    }

    #[test]
    fn compare_license_information_backwards() {
        let some_software = SomeSoftware {};
        let other_software = OtherSoftware {};

        assert!(compare_license_types(other_software, some_software));
    }
}
```

### 63. traits/traits5.rs

参考 [通过 `+` 指定多个 trait bound](https://kaisery.github.io/trpl-zh-cn/ch10-02-traits.html#通过--指定多个-trait-bound) 一节

```diff
pub trait SomeTrait {
    fn some_function(&self) -> bool {
        true
    }
}

pub trait OtherTrait {
    fn other_function(&self) -> bool {
        true
    }
}

struct SomeStruct {}
struct OtherStruct {}

impl SomeTrait for SomeStruct {}
impl OtherTrait for SomeStruct {}
impl SomeTrait for OtherStruct {}
impl OtherTrait for OtherStruct {}

// YOU MAY ONLY CHANGE THE NEXT LINE
+ fn some_func(item: (impl SomeTrait + OtherTrait)) -> bool {
    item.some_function() && item.other_function()
}

fn main() {
    some_func(SomeStruct {});
    some_func(OtherStruct {});
}
```

### 64. quiz3.rs

没懂啥意思，多加了一个函数输出等级，这是最快的方法。

```diff
pub struct ReportCard {
    pub grade: f32,
    pub student_name: String,
    pub student_age: u8,
}

impl ReportCard {
    pub fn print(&self) -> String {
        format!("{} ({}) - achieved a grade of {}",
            &self.student_name, &self.student_age, &self.grade)
    }
+    pub fn printalphabet(&self) -> String {
+        let mut alphabet = String::from("A+");
+        if &self.grade > &5.0 {
+            alphabet = String::from("A+");
+        } else if &self.grade > &4.5 {
+            alphabet = String::from("A");
+        }
+        format!("{} ({}) - achieved a grade of {}",
+            &self.student_name, &self.student_age, alphabet)
+    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn generate_numeric_report_card() {
        let report_card = ReportCard {
            grade: 2.1,
            student_name: "Tom Wriggle".to_string(),
            student_age: 12,
        };
        assert_eq!(
            report_card.print(),
            "Tom Wriggle (12) - achieved a grade of 2.1"
        );
    }

    #[test]
    fn generate_alphabetic_report_card() {
        // TODO: Make sure to change the grade here after you finish the exercise.
        let report_card = ReportCard {
-            grade: 2.1,
+            grade: 5.5,
            student_name: "Gary Plotter".to_string(),
            student_age: 11,
        };
        assert_eq!(
-            report_card.print(),
+            report_card.printalphabet(),
            "Gary Plotter (11) - achieved a grade of A+"
        );
    }
}
```

### 65. tests/tests1.rs

```diff
#[cfg(test)]
mod tests {
    #[test]
    fn you_can_assert() {
-        assert!();
+        assert!(1 == 1);
    }
}
```

### 66. tests/tests2.rs

```diff
#[cfg(test)]
mod tests {
    #[test]
    fn you_can_assert_eq() {
+        assert_eq!(1, 1);
    }
}
```

### 67. tests/tests3.rs

```diff
pub fn is_even(num: i32) -> bool {
    num % 2 == 0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn is_true_when_even() {
+        assert!(is_even(5) == false);
    }

    #[test]
    fn is_false_when_odd() {
+        assert!(is_even(4) == true);
    }
}
```

### 68. lifetimes/lifetimes1.rs

不知道最后返回值是 x 还是 y，所以不确定生命周期有多长。不知道传入的引用的具体生命周期，所以不能通过观察作用域来确定返回的引用是否总是有效。增加泛型生命周期参数来定义引用间的关系以便借用检查器可以进行分析。

```diff
-fn longest(x: &str, y: &str) -> &str {
+fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

fn main() {
    let string1 = String::from("abcd");
    let string2 = "xyz";

    let result = longest(string1.as_str(), string2);
    println!("The longest string is '{}'", result);
}
```

### 69. lifetimes/lifetimes2.rs

`longest` 函数返回的引用的生命周期应该与传入参数的生命周期中较短那个保持一致。

```diff
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

fn main() {
    let string1 = String::from("long string is long");
    let result;
-    {
        let string2 = String::from("xyz");
        result = longest(string1.as_str(), string2.as_str());
-    }
    println!("The longest string is '{}'", result);
}
```

### 70. lifetimes/lifetimes3.rs

为结构体增加生命周期注解。

```diff
+struct Book<'a> {
+    author: &'a str,
+    title: &'a str,
+}

fn main() {
    let name = String::from("Jill Smith");
    let title = String::from("Fish Flying");
    let book = Book { author: &name, title: &title };

    println!("{} by {}", book.title, book.author);
}
```

### 71. standard_library_types/iterators1.rs

```diff
fn main () {
    let my_fav_fruits = vec!["banana", "custard apple", "avocado", "peach", "raspberry"];

+    let mut my_iterable_fav_fruits = my_fav_fruits.iter();   // TODO: Step 1

    assert_eq!(my_iterable_fav_fruits.next(), Some(&"banana"));
+    assert_eq!(my_iterable_fav_fruits.next(), Some(&"custard apple"));     // TODO: Step 2
    assert_eq!(my_iterable_fav_fruits.next(), Some(&"avocado"));
+    assert_eq!(my_iterable_fav_fruits.next(), Some(&"peach"));     // TODO: Step 3
    assert_eq!(my_iterable_fav_fruits.next(), Some(&"raspberry"));
+    assert_eq!(my_iterable_fav_fruits.next(), None);     // TODO: Step 4
}
```

### 72. standard_library_types/iterators2.rs

```diff
pub fn capitalize_first(input: &str) -> String {
    let mut c = input.chars();
    match c.next() {
        None => String::new(),
+        Some(first) => first.to_uppercase().to_string() + c.as_str(),
    }
}

// Step 2.
// Apply the `capitalize_first` function to a slice of string slices.
// Return a vector of strings.
// ["hello", "world"] -> ["Hello", "World"]
pub fn capitalize_words_vector(words: &[&str]) -> Vec<String> {
+    let mut result = vec![];
+    for i in words.iter() {
+        result.push(capitalize_first(i));
+    }
+    result
}

// Step 3.
// Apply the `capitalize_first` function again to a slice of string slices.
// Return a single string.
// ["hello", " ", "world"] -> "Hello World"
pub fn capitalize_words_string(words: &[&str]) -> String {
+    let mut result = String::new();
+    for i in words.iter() {
+        result = result + &capitalize_first(i);
+    }
+    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_success() {
        assert_eq!(capitalize_first("hello"), "Hello");
    }

    #[test]
    fn test_empty() {
        assert_eq!(capitalize_first(""), "");
    }

    #[test]
    fn test_iterate_string_vec() {
        let words = vec!["hello", "world"];
        assert_eq!(capitalize_words_vector(&words), ["Hello", "World"]);
    }

    #[test]
    fn test_iterate_into_string() {
        let words = vec!["hello", " ", "world"];
        assert_eq!(capitalize_words_string(&words), "Hello World");
    }
}
```

### 73. standard_library_types/iterators3.rs

```diff
#[derive(Debug, PartialEq, Eq)]
pub enum DivisionError {
    NotDivisible(NotDivisibleError),
    DivideByZero,
}

#[derive(Debug, PartialEq, Eq)]
pub struct NotDivisibleError {
    dividend: i32,
    divisor: i32,
}

// Calculate `a` divided by `b` if `a` is evenly divisible by `b`.
// Otherwise, return a suitable error.
pub fn divide(a: i32, b: i32) -> Result<i32, DivisionError> {
+    if b == 0 {
+        return Err(DivisionError::DivideByZero);
+    }
+    let result = a / b;
+    if result * b != a {
+        Err(DivisionError::NotDivisible(NotDivisibleError{dividend: a, divisor: b}))
+    } else {
+        Ok(result)
+    }
}

// Complete the function and return a value of the correct type so the test passes.
// Desired output: Ok([1, 11, 1426, 3])
+fn result_with_list() -> Result<Vec<i32>, DivisionError> {
    let numbers = vec![27, 297, 38502, 81];
+    let division_results = numbers.into_iter().map(|n| divide(n, 27).unwrap()).collect();
+    Ok(division_results)
}

// Complete the function and return a value of the correct type so the test passes.
// Desired output: [Ok(1), Ok(11), Ok(1426), Ok(3)]
+fn list_of_results() -> Vec<Result<i32, DivisionError>> {
    let numbers = vec![27, 297, 38502, 81];
+    let division_results = numbers.into_iter().map(|n| divide(n, 27)).collect();
+    division_results
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_success() {
        assert_eq!(divide(81, 9), Ok(9));
    }

    #[test]
    fn test_not_divisible() {
        assert_eq!(
            divide(81, 6),
            Err(DivisionError::NotDivisible(NotDivisibleError {
                dividend: 81,
                divisor: 6
            }))
        );
    }

    #[test]
    fn test_divide_by_0() {
        assert_eq!(divide(81, 0), Err(DivisionError::DivideByZero));
    }

    #[test]
    fn test_divide_0_by_something() {
        assert_eq!(divide(0, 81), Ok(0));
    }

    #[test]
    fn test_result_with_list() {
        assert_eq!(format!("{:?}", result_with_list()), "Ok([1, 11, 1426, 3])");
    }

    #[test]
    fn test_list_of_results() {
        assert_eq!(
            format!("{:?}", list_of_results()),
            "[Ok(1), Ok(11), Ok(1426), Ok(3)]"
        );
    }
}
```

### 74. standard_library_types/iterators4.rs

fold 函数详解：https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.fold

```diff
pub fn factorial(num: u64) -> u64 {
    // Complete this function to return the factorial of num
    // Do not use:
    // - return
    // Try not to use:
    // - imperative style loops (for, while)
    // - additional variables
    // For an extra challenge, don't use:
    // - recursion
    // Execute `rustlings hint iterators4` for hints.
+    (1..num + 1)
+        .into_iter()
+        .fold(1, |a, b| a * b)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn factorial_of_0() {
        assert_eq!(1, factorial(0));
    }

    #[test]
    fn factorial_of_1() {
        assert_eq!(1, factorial(1));
    }
    #[test]
    fn factorial_of_2() {
        assert_eq!(2, factorial(2));
    }

    #[test]
    fn factorial_of_4() {
        assert_eq!(24, factorial(4));
    }
}
```

### 75. standard_library_types/iterators5.rs

```diff
use std::collections::HashMap;

#[derive(Clone, Copy, PartialEq, Eq)]
enum Progress {
    None,
    Some,
    Complete,
}

fn count_for(map: &HashMap<String, Progress>, value: Progress) -> usize {
    let mut count = 0;
    for val in map.values() {
        if val == &value {
            count += 1;
        }
    }
    count
}

fn count_iterator(map: &HashMap<String, Progress>, value: Progress) -> usize {
    // map is a hashmap with String keys and Progress values.
    // map = { "variables1": Complete, "from_str": None, ... }
+    count_for(map, value)
}

fn count_collection_for(collection: &[HashMap<String, Progress>], value: Progress) -> usize {
    let mut count = 0;
    for map in collection {
        for val in map.values() {
            if val == &value {
                count += 1;
            }
        }
    }
    count
}

fn count_collection_iterator(collection: &[HashMap<String, Progress>], value: Progress) -> usize {
    // collection is a slice of hashmaps.
    // collection = [{ "variables1": Complete, "from_str": None, ... },
    //     { "variables2": Complete, ... }, ... ]
+    count_collection_for(collection, value)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn count_complete() {
        let map = get_map();
        assert_eq!(3, count_iterator(&map, Progress::Complete));
    }

    #[test]
    fn count_equals_for() {
        let map = get_map();
        assert_eq!(
            count_for(&map, Progress::Complete),
            count_iterator(&map, Progress::Complete)
        );
    }

    #[test]
    fn count_collection_complete() {
        let collection = get_vec_map();
        assert_eq!(
            6,
            count_collection_iterator(&collection, Progress::Complete)
        );
    }

    #[test]
    fn count_collection_equals_for() {
        let collection = get_vec_map();
        assert_eq!(
            count_collection_for(&collection, Progress::Complete),
            count_collection_iterator(&collection, Progress::Complete)
        );
    }

    fn get_map() -> HashMap<String, Progress> {
        use Progress::*;

        let mut map = HashMap::new();
        map.insert(String::from("variables1"), Complete);
        map.insert(String::from("functions1"), Complete);
        map.insert(String::from("hashmap1"), Complete);
        map.insert(String::from("arc1"), Some);
        map.insert(String::from("as_ref_mut"), None);
        map.insert(String::from("from_str"), None);

        map
    }

    fn get_vec_map() -> Vec<HashMap<String, Progress>> {
        use Progress::*;

        let map = get_map();

        let mut other = HashMap::new();
        other.insert(String::from("variables2"), Complete);
        other.insert(String::from("functions2"), Complete);
        other.insert(String::from("if1"), Complete);
        other.insert(String::from("from_into"), None);
        other.insert(String::from("try_from_into"), None);

        vec![map, other]
    }
}
```

### 76. standard_library_types/box1.rs

```diff
+ use List::Nil;

#[derive(PartialEq, Debug)]
pub enum List {
    Cons(i32, Box<List>),
    Nil,
}

fn main() {
    println!("This is an empty cons list: {:?}", create_empty_list());
    println!(
        "This is a non-empty cons list: {:?}",
        create_non_empty_list()
    );
}

pub fn create_empty_list() -> List {
+    List::Nil
}

pub fn create_non_empty_list() -> List {
+    List::Cons(1, Box::new(Nil))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_empty_list() {
        assert_eq!(List::Nil, create_empty_list())
    }

    #[test]
    fn test_create_non_empty_list() {
        assert_ne!(create_empty_list(), create_non_empty_list())
    }
}
```

### 77. standard_library_types/arc1.rs

```diff
#![forbid(unused_imports)] // Do not change this, (or the next) line.
use std::sync::Arc;
use std::thread;

fn main() {
    let numbers: Vec<_> = (0..100u32).collect();
+    let shared_numbers = Arc::new(numbers);
    let mut joinhandles = Vec::new();

    for offset in 0..8 {
+        let child_numbers = Arc::clone(&shared_numbers);
        joinhandles.push(thread::spawn(move || {
            let sum: u32 = child_numbers.iter().filter(|n| *n % 8 == offset).sum();
            println!("Sum of offset {} is {}", offset, sum);
        }));
    }
    for handle in joinhandles.into_iter() {
        handle.join().unwrap();
    }
}
```

### 78. standard_library_types/rc1.rs

```diff
use std::rc::Rc;

#[derive(Debug)]
struct Sun {}

#[derive(Debug)]
enum Planet {
    Mercury(Rc<Sun>),
    Venus(Rc<Sun>),
    Earth(Rc<Sun>),
    Mars(Rc<Sun>),
    Jupiter(Rc<Sun>),
    Saturn(Rc<Sun>),
    Uranus(Rc<Sun>),
    Neptune(Rc<Sun>),
}

impl Planet {
    fn details(&self) {
        println!("Hi from {:?}!", self)
    }
}

fn main() {
    let sun = Rc::new(Sun {});
    println!("reference count = {}", Rc::strong_count(&sun)); // 1 reference

    let mercury = Planet::Mercury(Rc::clone(&sun));
    println!("reference count = {}", Rc::strong_count(&sun)); // 2 references
    mercury.details();

    let venus = Planet::Venus(Rc::clone(&sun));
    println!("reference count = {}", Rc::strong_count(&sun)); // 3 references
    venus.details();

    let earth = Planet::Earth(Rc::clone(&sun));
    println!("reference count = {}", Rc::strong_count(&sun)); // 4 references
    earth.details();

    let mars = Planet::Mars(Rc::clone(&sun));
    println!("reference count = {}", Rc::strong_count(&sun)); // 5 references
    mars.details();

    let jupiter = Planet::Jupiter(Rc::clone(&sun));
    println!("reference count = {}", Rc::strong_count(&sun)); // 6 references
    jupiter.details();

    // TODO
+    let saturn = Planet::Saturn(Rc::clone(&sun));
    println!("reference count = {}", Rc::strong_count(&sun)); // 7 references
    saturn.details();

    // TODO
+    let uranus = Planet::Uranus(Rc::clone(&sun));
    println!("reference count = {}", Rc::strong_count(&sun)); // 8 references
    uranus.details();

    // TODO
+    let neptune = Planet::Neptune(Rc::clone(&sun));
    println!("reference count = {}", Rc::strong_count(&sun)); // 9 references
    neptune.details();

    assert_eq!(Rc::strong_count(&sun), 9);

    drop(neptune);
    println!("reference count = {}", Rc::strong_count(&sun)); // 8 references

    drop(uranus);
    println!("reference count = {}", Rc::strong_count(&sun)); // 7 references

    drop(saturn);
    println!("reference count = {}", Rc::strong_count(&sun)); // 6 references

    drop(jupiter);
    println!("reference count = {}", Rc::strong_count(&sun)); // 5 references

    drop(mars);
    println!("reference count = {}", Rc::strong_count(&sun)); // 4 references
    
    // TODO
+    drop(earth);
    println!("reference count = {}", Rc::strong_count(&sun)); // 3 references
    
    // TODO
+    drop(venus);
    println!("reference count = {}", Rc::strong_count(&sun)); // 2 references
    
    // TODO
+    drop(mercury);
    println!("reference count = {}", Rc::strong_count(&sun)); // 1 reference

    assert_eq!(Rc::strong_count(&sun), 1);
}
```

### 79. standard_library_types/cow1.rs

不太清楚原因，还要在复习一下。

```diff

use std::borrow::Cow;

fn abs_all<'a, 'b>(input: &'a mut Cow<'b, [i32]>) -> &'a mut Cow<'b, [i32]> {
    for i in 0..input.len() {
        let v = input[i];
        if v < 0 {
            // Clones into a vector if not already owned.
            input.to_mut()[i] = -v;
        }
    }
    input
}

fn main() {
    // No clone occurs because `input` doesn't need to be mutated.
    let slice = [0, 1, 2];
    let mut input = Cow::from(&slice[..]);
    match abs_all(&mut input) {
        Cow::Borrowed(_) => println!("I borrowed the slice!"),
        _ => panic!("expected borrowed value"),
    }

    // Clone occurs because `input` needs to be mutated.
    let slice = [-1, 0, 1];
    let mut input = Cow::from(&slice[..]);
    match abs_all(&mut input) {
        Cow::Owned(_) => println!("I modified the slice and now own it!"),
        _ => panic!("expected owned value"),
    }

    // No clone occurs because `input` is already owned.
    let slice = vec![-1, 0, 1];
    let mut input = Cow::from(slice);
    match abs_all(&mut input) {
        // TODO
-        Cow::Borrowed(_) => println!("I own this slice!"),
+        Cow::Owned(_) => println!("I own this slice!"),
        _ => panic!("expected borrowed value"),
    }
}
```

### 80. threads/threads1.rs

```diff
use std::thread;
use std::time::Duration;


fn main() {

    let mut handles = vec![];
    for i in 0..10 {
-        thread::spawn(move || {
+        let handle = thread::spawn(move || {
            thread::sleep(Duration::from_millis(250));
            println!("thread {} is complete", i);
        });
+        handles.push(handle);
    }

    let mut completed_threads = 0;
    for handle in handles {
        // TODO: a struct is returned from thread::spawn, can you use it?
        completed_threads += 1;
    }

    if completed_threads != 10 {
        panic!("Oh no! All the spawned threads did not finish!");
    }
}
```

### 81. threads/threads2.rs

```diff
+ use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

struct JobStatus {
    jobs_completed: u32,
}

fn main() {
+    let status = Arc::new(Mutex::new(JobStatus { jobs_completed: 0 }));
    let mut handles = vec![];
    for _ in 0..10 {
        let status_shared = Arc::clone(&status);
        let handle = thread::spawn(move || {
            thread::sleep(Duration::from_millis(250));
            // TODO: You must take an action before you update a shared value
+            status_shared.lock().unwrap().jobs_completed += 1;
        });
        handles.push(handle);
    }
    for handle in handles {
        handle.join().unwrap();
        // TODO: Print the value of the JobStatus.jobs_completed. Did you notice anything
        // interesting in the output? Do you have to 'join' on all the handles?
+        println!("jobs completed {}", status.lock().unwrap().jobs_completed);
    }
}
```

### 82. threads/threads3.rs

`mpsc`是 *multiple producer, single consumer* 的缩写。可以运用 `mpsc` 来扩展示例 16-10 中的代码来创建向同一接收者发送值的多个线程。这可以通过克隆信道的发送端来做到。注释那两行也可以。

```diff
use std::sync::mpsc;
use std::sync::Arc;
use std::thread;
use std::time::Duration;

struct Queue {
    length: u32,
    first_half: Vec<u32>,
    second_half: Vec<u32>,
}

impl Queue {
    fn new() -> Self {
        Queue {
            length: 10,
            first_half: vec![1, 2, 3, 4, 5],
            second_half: vec![6, 7, 8, 9, 10],
        }
    }
}

fn send_tx(q: Queue, tx: mpsc::Sender<u32>) -> () {
    let qc = Arc::new(q);
    let qc1 = Arc::clone(&qc);
    let qc2 = Arc::clone(&qc);
+    // let tx1 = mpsc::Sender::clone(&tx);
+    // let tx2 = mpsc::Sender::clone(&tx);
+    let tx1 = tx.clone();
+    let tx2 = tx.clone();
    thread::spawn(move || {
        for val in &qc1.first_half {
            println!("sending {:?}", val);
+            tx1.send(*val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    thread::spawn(move || {
        for val in &qc2.second_half {
            println!("sending {:?}", val);
+            tx2.send(*val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });
}

fn main() {
    let (tx, rx) = mpsc::channel();
    let queue = Queue::new();
    let queue_length = queue.length;

    send_tx(queue, tx);

    let mut total_received: u32 = 0;
    for received in rx {
        println!("Got: {}", received);
        total_received += 1;
    }

    println!("total numbers received: {}", total_received);
    assert_eq!(total_received, queue_length)
}
```

### 83. macros/macros1.rs

调用宏时，宏名后面需要加上感叹号。

```diff
macro_rules! my_macro {
    () => {
        println!("Check out my macro!");
    };
}

fn main() {
+    my_macro!();
}
```

### 84. macros/macros2.rs

宏和函数的最后一个重要的区别是：在一个文件里调用宏 **之前** 必须定义它，或将其引入作用域，而函数则可以在任何地方定义和调用。改成跟 83 题一样就行。

### 85. macros/macros3.rs

在模块中定义的宏，在其他模块中是不可见的。

```diff
+ #[macro_use]
mod macros {
    macro_rules! my_macro {
        () => {
            println!("Check out my macro!");
        };
    }
}

fn main() {
    my_macro!();
}
```

### 86. macros/macros4.rs

不同模式之间用分号分隔。

```diff
macro_rules! my_macro {
    () => {
        println!("Check out my macro!");
+    };
    ($val:expr) => {
        println!("Look at this other macro: {}", $val);
    }
}

fn main() {
    my_macro!();
    my_macro!(7777);
}
```

### 87. clippy/clippy1.rs

直接使用系统自带的常数。

```diff
+ use std::f32::consts::PI;

fn main() {
-    let pi = 3.14f32;
    let radius = 5.00f32;

-    let area = pi * f32::powi(radius, 2);
+    let area = PI * f32::powi(radius, 2);

    println!(
        "The area of a circle with radius {:.2} is {:.5}!",
        radius, area
    )
}
```

### 88. clippy/clippy2.rs

根据报错提示替换。

```diff
fn main() {
    let mut res = 42;
    let option = Some(12);
+    if let Some(x) = option {
        res += x;
    }
    println!("{}", res);
}
```

### 89. clippy/clippy3.rs

```diff
+ use std::mem::swap;
#[allow(unused_variables, unused_assignments)]
fn main() {
    let my_option: Option<()> = None;
+    // if my_option.is_none() {
+    //     my_option.unwrap();
+    // }

    let my_arr = &[
-        -1, -2, -3
+        -1, -2, -3,
        -4, -5, -6
    ];
    println!("My array! Here it is: {:?}", my_arr);

+    let my_empty_vec: Option<()> = {
+        vec![1, 2, 3, 4, 5].clear();
+        Some(())
+    };
    println!("This Vec is empty, see? {:?}", my_empty_vec);

    let mut value_a = 45;
    let mut value_b = 66;
    // Let's swap these two!
+    swap(&mut value_a, &mut value_b);
+    // value_a = value_b;
+    // value_b = value_a;
    println!("value a: {}; value b: {}", value_a, value_b);
}
```

### 90. conversions/using_as.rs

显式类型转换

```diff
fn average(values: &[f64]) -> f64 {
    let total = values.iter().sum::<f64>();
+    total / values.len() as f64
}

fn main() {
    let values = [3.5, 0.3, 13.0, 11.7];
    println!("{}", average(&values));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn returns_proper_type_and_value() {
        assert_eq!(average(&[3.5, 0.3, 13.0, 11.7]), 7.125);
    }
}
```

### 91. conversions/from_into.rs

`parse` 返回一个 `Result` 类型，而 `Result` 是一个拥有 `Ok` 或 `Err` 成员的枚举。使用 `parse()` 方法尝试将该字符串转换为 `usize` 类型。如果转换成功，它将使用转换后的年龄创建一个 `Person` 实例。否则，它将执行 `else` 块中的代码。

这里使用了 `if let` 语句的原因是因为调用 `parse()` 方法会返回一个 `Result` 类型的值，它表示转换是否成功。如果转换成功，`Result` 中封装了成功转换后的值。如果转换失败，`Result` 封装了错误信息。 `if let` 语句允许我们在转换成功时提取封装在 `Result` 中的值，并在转换失败时执行其他操作。这种方法可以更方便地处理 `Result` 类型的值，而不需要使用传统的 `match` 语句。

```diff

impl From<&str> for Person {
    fn from(s: &str) -> Person {
+        let s = s.split(',').collect::<Vec<&str>>();
+        if s.len() != 2 || s[0].len() == 0 {
+            return Person::default();
+        }
+        if let Ok(age) = s[1].to_string().parse::<usize>(){
+            Person{
+                name: String::from(s[0]),
+                age:age
+            }
+        }
+        else {
+            return Person::default();
+        }
    }
}

fn main() {
    // Use the `from` function
    let p1 = Person::from("Mark,20");
    // Since From is implemented for Person, we should be able to use Into
    let p2: Person = "Gerald,70".into();
    println!("{:?}", p1);
    println!("{:?}", p2);
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_default() {
        // Test that the default person is 30 year old John
        let dp = Person::default();
        assert_eq!(dp.name, "John");
        assert_eq!(dp.age, 30);
    }
    #[test]
    fn test_bad_convert() {
        // Test that John is returned when bad string is provided
        let p = Person::from("");
        assert_eq!(p.name, "John");
        assert_eq!(p.age, 30);
    }
    #[test]
    fn test_good_convert() {
        // Test that "Mark,20" works
        let p = Person::from("Mark,20");
        assert_eq!(p.name, "Mark");
        assert_eq!(p.age, 20);
    }
    #[test]
    fn test_bad_age() {
        // Test that "Mark,twenty" will return the default person due to an error in parsing age
        let p = Person::from("Mark,twenty");
        assert_eq!(p.name, "John");
        assert_eq!(p.age, 30);
    }

    #[test]
    fn test_missing_comma_and_age() {
        let p: Person = Person::from("Mark");
        assert_eq!(p.name, "John");
        assert_eq!(p.age, 30);
    }

    #[test]
    fn test_missing_age() {
        let p: Person = Person::from("Mark,");
        assert_eq!(p.name, "John");
        assert_eq!(p.age, 30);
    }

    #[test]
    fn test_missing_name() {
        let p: Person = Person::from(",1");
        assert_eq!(p.name, "John");
        assert_eq!(p.age, 30);
    }

    #[test]
    fn test_missing_name_and_age() {
        let p: Person = Person::from(",");
        assert_eq!(p.name, "John");
        assert_eq!(p.age, 30);
    }

    #[test]
    fn test_missing_name_and_invalid_age() {
        let p: Person = Person::from(",one");
        assert_eq!(p.name, "John");
        assert_eq!(p.age, 30);
    }

    #[test]
    fn test_trailing_comma() {
        let p: Person = Person::from("Mike,32,");
        assert_eq!(p.name, "John");
        assert_eq!(p.age, 30);
    }

    #[test]
    fn test_trailing_comma_and_some_string() {
        let p: Person = Person::from("Mike,32,man");
        assert_eq!(p.name, "John");
        assert_eq!(p.age, 30);
    }
}

```

### 92. conversions/from_str.rs

```diff
use std::num::ParseIntError;
use std::str::FromStr;

#[derive(Debug, PartialEq)]
struct Person {
    name: String,
    age: usize,
}

// We will use this error type for the `FromStr` implementation.
#[derive(Debug, PartialEq)]
enum ParsePersonError {
    // Empty input string
    Empty,
    // Incorrect number of fields
    BadLen,
    // Empty name field
    NoName,
    // Wrapped error from parse::<usize>()
    ParseInt(ParseIntError),
}

// I AM NOT DONE

// Steps:
// 1. If the length of the provided string is 0, an error should be returned
// 2. Split the given string on the commas present in it
// 3. Only 2 elements should be returned from the split, otherwise return an error
// 4. Extract the first element from the split operation and use it as the name
// 5. Extract the other element from the split operation and parse it into a `usize` as the age
//    with something like `"4".parse::<usize>()`
// 6. If while extracting the name and the age something goes wrong, an error should be returned
// If everything goes well, then return a Result of a Person object
//
// As an aside: `Box<dyn Error>` implements `From<&'_ str>`. This means that if you want to return a
// string error message, you can do so via just using return `Err("my error message".into())`.

impl FromStr for Person {
    type Err = ParsePersonError;
    fn from_str(s: &str) -> Result<Person, Self::Err> {
+        if s.len() == 0 {
+            return Err(ParsePersonError::Empty);
+        }
+        let s = s.split(",").collect::<Vec<_>>();
+        if s.len() != 2 {return Err(ParsePersonError::BadLen)}
+        if s[0] == "" {
+            return Err(ParsePersonError::NoName);
+        }
+        let age = match s[1].parse::<usize>() {
+            Ok(age)  => age,
+            Err(e) => return Err(ParsePersonError::ParseInt(e)),
+        };
+        Ok(Person{
+            name: String::from(s[0]),
+            age: age
+        })
    }
}

fn main() {
    let p = "Mark,20".parse::<Person>().unwrap();
    println!("{:?}", p);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn empty_input() {
        assert_eq!("".parse::<Person>(), Err(ParsePersonError::Empty));
    }
    #[test]
    fn good_input() {
        let p = "John,32".parse::<Person>();
        assert!(p.is_ok());
        let p = p.unwrap();
        assert_eq!(p.name, "John");
        assert_eq!(p.age, 32);
    }
    #[test]
    fn missing_age() {
        assert!(matches!(
            "John,".parse::<Person>(),
            Err(ParsePersonError::ParseInt(_))
        ));
    }

    #[test]
    fn invalid_age() {
        assert!(matches!(
            "John,twenty".parse::<Person>(),
            Err(ParsePersonError::ParseInt(_))
        ));
    }

    #[test]
    fn missing_comma_and_age() {
        assert_eq!("John".parse::<Person>(), Err(ParsePersonError::BadLen));
    }

    #[test]
    fn missing_name() {
        assert_eq!(",1".parse::<Person>(), Err(ParsePersonError::NoName));
    }

    #[test]
    fn missing_name_and_age() {
        assert!(matches!(
            ",".parse::<Person>(),
            Err(ParsePersonError::NoName | ParsePersonError::ParseInt(_))
        ));
    }

    #[test]
    fn missing_name_and_invalid_age() {
        assert!(matches!(
            ",one".parse::<Person>(),
            Err(ParsePersonError::NoName | ParsePersonError::ParseInt(_))
        ));
    }

    #[test]
    fn trailing_comma() {
        assert_eq!("John,32,".parse::<Person>(), Err(ParsePersonError::BadLen));
    }

    #[test]
    fn trailing_comma_and_some_string() {
        assert_eq!(
            "John,32,man".parse::<Person>(),
            Err(ParsePersonError::BadLen)
        );
    }
}

```

### 93. conversions/try_from_into.rs

```diff
use std::convert::{TryFrom, TryInto};

#[derive(Debug, PartialEq)]
struct Color {
    red: u8,
    green: u8,
    blue: u8,
}

// We will use this error type for these `TryFrom` conversions.
#[derive(Debug, PartialEq)]
enum IntoColorError {
    // Incorrect length of slice
    BadLen,
    // Integer conversion error
    IntConversion,
}

// I AM NOT DONE

// Your task is to complete this implementation
// and return an Ok result of inner type Color.
// You need to create an implementation for a tuple of three integers,
// an array of three integers, and a slice of integers.
//
// Note that the implementation for tuple and array will be checked at compile time,
// but the slice implementation needs to check the slice length!
// Also note that correct RGB color values must be integers in the 0..=255 range.

// Tuple implementation
impl TryFrom<(i16, i16, i16)> for Color {
    type Error = IntoColorError;
    fn try_from(tuple: (i16, i16, i16)) -> Result<Self, Self::Error> {
+        match tuple {
+            (r @ 0..=255, g @ 0..=255, b @ 0..=255) => Ok(Color {
+                red: r as u8,
+                green: g as u8,
+                blue: b as u8,
+            }),
+            _ => Err(IntoColorError::IntConversion),
+        }
    }
}

// Array implementation
impl TryFrom<[i16; 3]> for Color {
    type Error = IntoColorError;
    fn try_from(arr: [i16; 3]) -> Result<Self, Self::Error> {
+        for num in arr.iter() {
+            if !(&0 <= num && num <= &255) {
+                return Err(IntoColorError::IntConversion)
+            }
+        }
+        Ok(Color { red: arr[0] as u8, green: arr[1] as u8, blue: arr[2] as u8 })
    }
}

// Slice implementation
impl TryFrom<&[i16]> for Color {
    type Error = IntoColorError;
    fn try_from(slice: &[i16]) -> Result<Self, Self::Error> {
+        if slice.len() != 3 {
+            return Err(IntoColorError::BadLen)
+        }

+        for num in slice.iter() {
+            if !(&0 <= num && num <= &255) {
+                return Err(IntoColorError::IntConversion)
+            }
+        }

+        Ok(Color { red: slice[0] as u8, green: slice[1] as u8, blue: slice[2] as u8 })
    }
}

fn main() {
    // Use the `try_from` function
    let c1 = Color::try_from((183, 65, 14));
    println!("{:?}", c1);

    // Since TryFrom is implemented for Color, we should be able to use TryInto
    let c2: Result<Color, _> = [183, 65, 14].try_into();
    println!("{:?}", c2);

    let v = vec![183, 65, 14];
    // With slice we should use `try_from` function
    let c3 = Color::try_from(&v[..]);
    println!("{:?}", c3);
    // or take slice within round brackets and use TryInto
    let c4: Result<Color, _> = (&v[..]).try_into();
    println!("{:?}", c4);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tuple_out_of_range_positive() {
        assert_eq!(
            Color::try_from((256, 1000, 10000)),
            Err(IntoColorError::IntConversion)
        );
    }
    #[test]
    fn test_tuple_out_of_range_negative() {
        assert_eq!(
            Color::try_from((-1, -10, -256)),
            Err(IntoColorError::IntConversion)
        );
    }
    #[test]
    fn test_tuple_sum() {
        assert_eq!(
            Color::try_from((-1, 255, 255)),
            Err(IntoColorError::IntConversion)
        );
    }
    #[test]
    fn test_tuple_correct() {
        let c: Result<Color, _> = (183, 65, 14).try_into();
        assert!(c.is_ok());
        assert_eq!(
            c.unwrap(),
            Color {
                red: 183,
                green: 65,
                blue: 14
            }
        );
    }
    #[test]
    fn test_array_out_of_range_positive() {
        let c: Result<Color, _> = [1000, 10000, 256].try_into();
        assert_eq!(c, Err(IntoColorError::IntConversion));
    }
    #[test]
    fn test_array_out_of_range_negative() {
        let c: Result<Color, _> = [-10, -256, -1].try_into();
        assert_eq!(c, Err(IntoColorError::IntConversion));
    }
    #[test]
    fn test_array_sum() {
        let c: Result<Color, _> = [-1, 255, 255].try_into();
        assert_eq!(c, Err(IntoColorError::IntConversion));
    }
    #[test]
    fn test_array_correct() {
        let c: Result<Color, _> = [183, 65, 14].try_into();
        assert!(c.is_ok());
        assert_eq!(
            c.unwrap(),
            Color {
                red: 183,
                green: 65,
                blue: 14
            }
        );
    }
    #[test]
    fn test_slice_out_of_range_positive() {
        let arr = [10000, 256, 1000];
        assert_eq!(
            Color::try_from(&arr[..]),
            Err(IntoColorError::IntConversion)
        );
    }
    #[test]
    fn test_slice_out_of_range_negative() {
        let arr = [-256, -1, -10];
        assert_eq!(
            Color::try_from(&arr[..]),
            Err(IntoColorError::IntConversion)
        );
    }
    #[test]
    fn test_slice_sum() {
        let arr = [-1, 255, 255];
        assert_eq!(
            Color::try_from(&arr[..]),
            Err(IntoColorError::IntConversion)
        );
    }
    #[test]
    fn test_slice_correct() {
        let v = vec![183, 65, 14];
        let c: Result<Color, _> = Color::try_from(&v[..]);
        assert!(c.is_ok());
        assert_eq!(
            c.unwrap(),
            Color {
                red: 183,
                green: 65,
                blue: 14
            }
        );
    }
    #[test]
    fn test_slice_excess_length() {
        let v = vec![0, 0, 0, 0];
        assert_eq!(Color::try_from(&v[..]), Err(IntoColorError::BadLen));
    }
    #[test]
    fn test_slice_insufficient_length() {
        let v = vec![0, 0];
        assert_eq!(Color::try_from(&v[..]), Err(IntoColorError::BadLen));
    }
}
```

### 94. conversions/as_ref_mut.rs

AsRef 是干啥的？

```diff
+ fn byte_counter<T: AsRef<str>>(arg: T) -> usize {
    arg.as_ref().as_bytes().len()
}

// Obtain the number of characters (not bytes) in the given argument
// Add the AsRef trait appropriately as a trait bound
+ fn char_counter<T: AsRef<str>>(arg: T) -> usize {
    arg.as_ref().chars().count()
}

// Squares a number using as_mut(). Add the trait bound as is appropriate and
// implement the function body.
+ fn num_sq<T: AsMut<u32>>(arg: &mut T) {
+    *arg.as_mut() *= *arg.as_mut()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn different_counts() {
        let s = "Café au lait";
        assert_ne!(char_counter(s), byte_counter(s));
    }

    #[test]
    fn same_counts() {
        let s = "Cafe au lait";
        assert_eq!(char_counter(s), byte_counter(s));
    }

    #[test]
    fn different_counts_using_string() {
        let s = String::from("Café au lait");
        assert_ne!(char_counter(s.clone()), byte_counter(s));
    }

    #[test]
    fn same_counts_using_string() {
        let s = String::from("Cafe au lait");
        assert_eq!(char_counter(s.clone()), byte_counter(s));
    }

    #[test]
    fn mult_box() {
        let mut num: Box<u32> = Box::new(3);
        num_sq(&mut num);
        assert_eq!(*num, 9);
    }
}

```

完成✅

```
🎉 All exercises completed! 🎉

+----------------------------------------------------+
|          You made it to the Fe-nish line!          |
+--------------------------  ------------------------+
                          \\/
     ▒▒          ▒▒▒▒▒▒▒▒      ▒▒▒▒▒▒▒▒          ▒▒
   ▒▒▒▒  ▒▒    ▒▒        ▒▒  ▒▒        ▒▒    ▒▒  ▒▒▒▒
   ▒▒▒▒  ▒▒  ▒▒            ▒▒            ▒▒  ▒▒  ▒▒▒▒
 ░░▒▒▒▒░░▒▒  ▒▒            ▒▒            ▒▒  ▒▒░░▒▒▒▒
   ▓▓▓▓▓▓▓▓  ▓▓      ▓▓██  ▓▓  ▓▓██      ▓▓  ▓▓▓▓▓▓▓▓
     ▒▒▒▒    ▒▒      ████  ▒▒  ████      ▒▒░░  ▒▒▒▒
       ▒▒  ▒▒▒▒▒▒        ▒▒▒▒▒▒        ▒▒▒▒▒▒  ▒▒
         ▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▒▒▒▒▒▒▒▒▓▓▒▒▓▓▒▒▒▒▒▒▒▒
           ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
             ▒▒▒▒▒▒▒▒▒▒██▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒▒
           ▒▒  ▒▒▒▒▒▒▒▒▒▒██████▒▒▒▒▒▒▒▒▒▒  ▒▒
         ▒▒    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    ▒▒
       ▒▒    ▒▒    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    ▒▒    ▒▒
       ▒▒  ▒▒    ▒▒                  ▒▒    ▒▒  ▒▒
           ▒▒  ▒▒                      ▒▒  ▒▒
```

## 基于 Rust 语言进行操作系统内核实验

实验文档：https://learningos.github.io/rust-based-os-comp2022/0setup-devel-env.html

排行榜：https://learningos.github.io/classroom-grading/

### lab0-0-setup-env-run-os1

我的实验代码仓库：https://github.com/LearningOS/lab0-0-setup-env-run-os1-yym68686

目前实验进行到第一阶段的第二步了，根据文档：https://github.com/LearningOS/rust-based-os-comp2022/blob/main/scheduling.md 的 step 2 基于Rust语言进行操作系统内核实验--based on qemu （大约14~31天）里面的具体步骤，点击链接生成一个 github classroom 环境。在形成的代码仓库里让 codespaces 在本地的 VSCode 打开。根据 [实验文档](https://learningos.github.io/rust-based-os-comp2022/chapter1/0intro.html#id4) 的提示，配置实验环境，先更新 apt 源：

```bash
sudo apt update
```

在项目根目录安装实验环境

```
make codespaces_setenv
```

进入第一个实验，运行项目

```bash
cd os1
make run LOG=TRACE
```



## 学习记录

### 11.10

计划：

- 完成 rustlings 练习
- 安装 rustlings 环境

成果：

- 安装了 rustlings，完成了 20 道练习题。

### 11.11

计划：

- rustlings 计划完成到 50 道练习题

成果：

- 完成到 34 题。

### 11.12

计划：

- rustlings 计划完成到 50 道练习题

成果：

- 计划完成到第 45 道练习题

### 11.13 - 11.14

休息

### 11.15

计划：

- 完成 rustlings 习题到 60 题。
- 找一下 RISC-V 资料，学一点。

成果：

- 了解了 RISC-V 的历史。

- 摩尔定律终结后，提高芯片的性能变得越来越困难。只能通过调整 ISA，为特定功能研发特定芯片，才能提高性价比。ISA 必须保留操作码空间以供未来的提升。
- rustlings 完成到第 50 题

### 11.16

计划：

- rustlings 完成到 60 题。

成果：

- rustlings 完成到 58 题。

### 11.17

计划：

- rustlings 完成到 70 题。

成果：

- rustlings 完成到 63 题。

### 11.18

计划：

- rustlings 完成到 70 题。

成果：

- rustlings 完成到 63 题。

### 11.19-11.22

休息

### 11.23

计划：

- rustlings 完成到 70 题。

成果：

- rustlings 完成到 70 题。

### 11.24

计划：

- rustlings 完成到 80 题。
- 阅读《计算机组成与设计（RISC-V版）》第一、二章。

成果：

- rustlings 完成到 76 题。

### 11.25

计划：

- rustlings 完成到 90 题。
- 阅读《计算机组成与设计（RISC-V版）》第一、二章。
- 自学 [RISC-V手册：一本开源指令集的指南](http://riscvbook.com/chinese/RISC-V-Reader-Chinese-v2p1.pdf) 重点是第10章

成果：

- rustlings 完成到 81 题

### 11.26-12.3

休息

### 12.4

计划：

- rustlings 完成到 94 题。
- 阅读《计算机组成与设计（RISC-V版）》第一、二章。
- 自学 [RISC-V手册：一本开源指令集的指南](http://riscvbook.com/chinese/RISC-V-Reader-Chinese-v2p1.pdf) 重点是第10章

成果：

- rustlings 完成到 94 题

### 12.5-12.6

休息

### 12.7

计划：

- 阅读《计算机组成与设计（RISC-V版）》第一、二章。
- 阅读 [RISC-V手册：一本开源指令集的指南](http://riscvbook.com/chinese/RISC-V-Reader-Chinese-v2p1.pdf) 第一章

成果：

- 读完 [RISC-V手册：一本开源指令集的指南](http://riscvbook.com/chinese/RISC-V-Reader-Chinese-v2p1.pdf) 第一章，第二章读了一点。
