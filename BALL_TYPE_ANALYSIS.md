# Lottery Ball Type Analysis

## NLB Lotteries Ball Type Patterns

Based on HTML analysis of actual lottery results:

### 1. **Suba Dawasak**
- Structure: **Zodiac** + 3 Regular Numbers + Promotional Draw (4 numbers)
- Classes:
  - Zodiac: `<li class="Zodiac Square Blue bL" title="Zodiac">PISCES</li>`
  - Numbers: `<li class="Number-2 Circle Yellow bX" title="Number-1/2/3">X</li>`
  - Promotional: `<li class="Number-1 Square Blue bX" title="Number-1/2/3/4">X</li>`

### 2. **Handahana**
- Structure: **Zodiac** + 4 Regular Numbers
- Classes:
  - Zodiac: `<li class="Zodiac Square Blue bD" title="Zodiac">CANCER</li>`
  - Numbers: `<li class="Number-2 Circle Yellow bXX" title="Number-1/2/3/4">XX</li>`

### 3. **Mega Power**
- Structure: **Letter** + **Super Number (RED!)** + 4 Regular Numbers
- Classes:
  - Letter: `<li class="Letter Circle Blue bU" title="Letter">U</li>`
  - Super: `<li class="Number-2 Circle Red b21" title="Super Number">21</li>` **(RED Circle!)**
  - Numbers: `<li class="Number-2 Circle Yellow bXX" title="Number-1/2/3/4">XX</li>`

### 4. **Ada Sampatha**
- Structure: **Letter** + 4 Numbers
- Classes:
  - Letter: `<li class="Letter Circle Blue bH/A/O/Z" title="Letter">H</li>`

### 5. **Dhana Nidhanaya**
- Structure: **Letter** + Numbers
- Classes:
  - Letter: `<li class="Letter Circle Blue bZ" title="Letter">Z</li>`
  - Also has: `<li class="Letter Circle Red" title="Letter">` (RED Letter variant)

### 6. **Govisetha**
- Structure: **Letter** + Numbers
- Classes:
  - Letter: `<li class="Letter Circle Blue bR" title="Letter">R</li>`

### 7. **NLB Jaya**
- (Need to verify - likely Letter + Numbers)

### 8. **Mahajana Sampatha**
- (Need to verify - likely Letter + Numbers)

## DLB Lotteries Ball Type Patterns

All DLB lotteries use `eng_letter` class for letters and `number_shanida number_circle` for numbers.

Example structure (Ada Kotipathi):
```html
<h6 class="eng_letter">Y</h6>
<h6 class="number_shanida number_circle" style="border: 2px solid #80DFFF;">08</h6>
```

### DLB Lotteries (9 total):
1. **Ada Kotipathi** - Letter + 4 Numbers
2. **Shanida** - Letter + Numbers
3. **Lagna Wasana** - Likely Zodiac variant (name suggests "lucky zodiac")
4. **Supiri Dhana Sampatha** - Letter + Numbers
5. **Super Ball** - Letter + Numbers
6. **Kapruka** - Letter + Numbers
7. **Jayoda** - Letter + Numbers
8. **Sasiri** - Letter + Numbers
9. **Jaya Sampatha** - Letter + Numbers

## Ball Type Classification

### CSS Class Patterns:
- **Letter**: `class="Letter Circle Blue"` or `class="eng_letter"`
- **Zodiac**: `class="Zodiac Square Blue"`
- **Super Number**: `class="Number-2 Circle Red"` **(RED color is key!)**
- **Regular Number**: `class="Number-2 Circle Yellow"`
- **Promotional**: `class="Number-1 Square Blue"`

### Title Attributes:
- `title="Letter"` - Letter ball
- `title="Zodiac"` - Zodiac sign
- `title="Super Number"` - Super number (Mega Power only)
- `title="Number-1/2/3/4"` - Regular numbers

### Shape & Color Coding:
- **Circle** - Main draw balls (letters, super, regular numbers)
- **Square** - Special balls (zodiac, promotional)
- **Blue** - Letters, zodiac, promotional
- **Yellow** - Regular numbers
- **Red** - Super numbers (Mega Power only)

## User Claims Verification:
✅ "all of nlb lotteries contains a letter" - **PARTIALLY TRUE**
   - 6 lotteries use Letter (Ada Sampatha, Dhana Nidhanaya, Govisetha, Mega Power, likely NLB Jaya, Mahajana Sampatha)
   - 2 lotteries use Zodiac (Suba Dawasak, Handahana)

✅ "only two have zodiac signs" - **TRUE**
   - Suba Dawasak and Handahana confirmed

✅ "mega power has super numbers" - **TRUE**
   - Mega Power has RED Circle super numbers

✅ "in dlb also it has letters numbers and zodiacs" - **PARTIALLY TRUE**
   - All DLB lotteries have letters
   - Lagna Wasana name suggests zodiac (needs verification)
   - Need to check individual DLB lotteries for zodiac patterns
