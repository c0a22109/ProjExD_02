import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1600, 900

delta = {  # 練習３：移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
def check_bound(obj_rct: pg.Rect):
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: # 横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: # 縦方向判定
        tate = False
    return yoko, tate

def main():
    # ウィンドウの初期化
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # 画像の読み込みと初期化
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_right = pg.image.load("ex02/fig/3.png")
    kk_img_left = pg.transform.flip(kk_img_right, True, False)
    kk_img_right = pg.transform.rotozoom(kk_img_right, 0, 2.0)
    kk_img_left = pg.transform.rotozoom(kk_img_left, 0, 2.0)
    kk_img_up = pg.transform.flip(kk_img_left, True, False)
    kk_img_up = pg.transform.rotozoom(kk_img_left, 90, 1.0)
    kk_img_down = pg.transform.rotozoom(kk_img_left, -90, 1.0)
    kk_img_up_right = pg.transform.rotozoom(kk_img_left, -45, 1.0)
    kk_img_down_right = pg.transform.rotozoom(kk_img_left, 45, 2.0)
    kk_img_up_left = pg.transform.rotozoom(kk_img_right, -135, 2.0)
    kk_img_down_left = pg.transform.rotozoom(kk_img_right, 135, 2.0)
    bb_img = pg.Surface((20, 20)) #練習１：透明のSurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #練習１：赤い半径10の円を作る
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5 #練習２：爆弾の速度    
    bb_img.set_colorkey((0, 0, 0)) #練習１：黒い部分を透明にする
    kk_img = kk_img_right

    # Rectが画面内にあるかどうかを判定する関数
    def is_inside_screen(rect):
        return (
            0 <= rect.left <= WIDTH and
            0 <= rect.right <= WIDTH and
            0 <= rect.top <= HEIGHT and
            0 <= rect.bottom <= HEIGHT
        )

    clock = pg.time.Clock()

    # こうかとんと爆弾の初期位置の設定
    kk_rect = kk_img.get_rect(topleft=(900, 400))

    # 移動の設定
    move_dict = {
        pg.K_UP: (0, -5), # 上矢印
        pg.K_DOWN: (0, 5), # 下矢印
        pg.K_LEFT: (-5, 0), # 左矢印
        pg.K_RIGHT: (5, 0), # 右矢印
        pg.K_UP | pg.K_RIGHT: (5, -5), # 右上
        pg.K_DOWN | pg.K_RIGHT: (5, 5), # 右下
        pg.K_DOWN | pg.K_LEFT: (0, 5), # 左下
        pg.K_UP | pg.K_LEFT: (0, -5) #左上
    }

    vx, vy = 5, 5
    accs = [a for a in range(1, 11)]

    font = pg.font.Font(None, 36)

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        # キーの押下状態リストを取得   
        key_lst = pg.key.get_pressed()

        # 合計移動量を求める
        total_movement = [0, 0]
        for key, movement in move_dict.items():
            if key_lst[key]:
                total_movement[0] += movement[0]
                total_movement[1] += movement[1]

        # こうかとんの位置を移動
        kk_rect.move_ip(*total_movement)

        if not is_inside_screen(kk_rect):
            kk_rect.move_ip(*[-movement for movement in total_movement])

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 練習４：横方向にはみ出たら
            vx *= -1
        if not tate:  # 練習４：縦方向にはみ出たら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        
        # こうかとんと爆弾が衝突したらreturn
        if kk_rect.colliderect(bb_rct):
            kk_img_collision = pg.image.load("ex02/fig/8.png")
            kk_img_collision = pg.transform.rotozoom(kk_img_collision, 0, 3.0)
            screen.blit(bg_img, [0, 0])
            screen.blit(kk_img_collision, kk_rect.topleft)
            pg.display.update()
            pg.time.wait(1000)
            return
        
        # 飛ぶ方向に応じてこうかとんを切り替える
        for key, movement in move_dict.items():
            if key_lst[key]:
                if movement[0] == 0 and movement[1] < 0:
                    kk_img = kk_img_up
                elif movement[0] == 0 and movement[1] > 0:
                    kk_img = kk_img_down
                if movement[0] > 0:
                    kk_img = kk_img_left
                elif movement[0] < 0:
                    kk_img = kk_img_right
                elif movement[0] < 0 and movement[1] < 0:
                    kk_img = kk_img_up_left
                elif movement[0] > 0 and movement[1] < 0:
                    kk_img = kk_img_up_right
                elif movement[0] < 0 and movement[1] > 0:
                    kk_img = kk_img_down_left
                elif movement[0] > 0 and movement[1] > 0:
                    kk_img = kk_img_down_right

        # 画面の描画
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rect.topleft)
        screen.blit(bb_img, bb_rct.topleft)


        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()