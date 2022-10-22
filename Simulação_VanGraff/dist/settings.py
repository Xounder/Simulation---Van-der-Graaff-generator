screen_width = 1280
screen_height = 720

x = screen_width/2 - 13
y = screen_height/2 - 30
offset_y = 60
charge_cor_pos = [[x, y + offset_y*3], [x, y + offset_y*2], [x, y + offset_y*1], [x, y]]
x = screen_width/2 + 10
charge_cor_pos_right =  [[x, y + offset_y*3], [x, y + offset_y*2], [x, y + offset_y*1], [x, y]]

charge_head = [[560, 330], [550, 290], [560, 230], [592, 198], [635, 185], [730, 290], [720, 330], [692, 198], [720, 230]]

charge_bas = [[40,0], [32, 26], [-40, 0], [-32, -26], [0, 40], [32, -26], [0, -40], [-32, 26], [0,0]]

# neutro e colisão esquerda, direita, cima, baixo
charge_bas_col = [['neg', 'pos', 'neg', 'pos', 'neg', 'pos', 'neg', 'pos', 'pos'], 
                        ['neg', 'neg', 'pos', 'pos', 'neg', 'neg', 'pos', 'pos', 'pos'],
                            ['pos', 'pos', 'neg', 'neg', 'pos', 'pos', 'neg', 'neg', 'pos'],
                                ['pos', 'pos', 'neg', 'neg', 'pos', 'neg', 'neg', 'pos', 'pos'],
                                    ['neg', 'neg', 'pos', 'pos', 'neg', 'pos', 'pos', 'neg', 'pos']]
