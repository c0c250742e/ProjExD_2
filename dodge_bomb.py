import os
import sys
import random
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect または 爆弾Rect
    戻り値：タプル（横方向判定結果, 縦方向判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:  # 横方向の判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:  # 縦方向の判定
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    DELTA = {
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
    }
    
    # === 【練習2：爆弾の作成】 ===
    bb_img = pg.Surface((20, 20))            # 20x20の空のSurfaceを作成
    bb_img.set_colorkey((0, 0, 0))           # 黒い部分を透明にする
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い円を描く
    bb_rct = bb_img.get_rect()               # 爆弾のRectを取得
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 初期位置をランダムに
    vx, vy = +5, +5                          # 爆弾の移動速度
    # ============================

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        # 【練習3：こうかとんが画面外に出ないようにする】
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 動く前の位置に戻す

        # === 【練習2・3：爆弾の移動と壁反射】 ===
        bb_rct.move_ip(vx, vy)  # 爆弾を移動させる
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向に出そうになったら
            vx *= -1  # 横の移動速度を反転
        if not tate:  # 縦方向に出そうになったら
            vy *= -1  # 縦の移動速度を反転
        screen.blit(bb_img, bb_rct)  # 爆弾を画面に描画
        # ======================================

        # === 【練習4：こうかとんと爆弾の衝突判定】 ===
        if kk_rct.colliderect(bb_rct):
            return  # 衝突したらmain関数を終了（ゲームオーバー）
        # ==========================================
        
        screen.blit(kk_img, kk_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
