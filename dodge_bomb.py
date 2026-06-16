import os
import sys
import random
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する関数
    引数 screen: 描画対象のスクリーンSurface
    """
    # 1. 黒い矩形用のSurface（画面サイズと同じ）を作り、黒で塗りつぶす
    bo_img = pg.Surface((WIDTH, HEIGHT))
    bo_img.fill((0, 0, 0))
    bo_img.set_alpha(150)  # 2. 半透明にする（0〜255）

    # 3.Game Overのフォント
    font = pg.font.Font(None, 80)
    txt_surf = font.render("Game Over", True, (255, 255, 255))
    txt_rect = txt_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # 4.泣いているこうかとん
    cry_kk_img = pg.image.load("fig/8.png")
    cry_kk_rect1 = cry_kk_img.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2))
    cry_kk_rect2 = cry_kk_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2))

    # 5.Surfaceにblit
    bo_img.blit(txt_surf, txt_rect)
    bo_img.blit(cry_kk_img, cry_kk_rect1)
    bo_img.blit(cry_kk_img, cry_kk_rect2)

    # 6.5秒待機
    screen.blit(bo_img, [0, 0])
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    
    """
    サイズ違いの爆弾Surfaceのリストと、加速度倍率のリストを返す関数
    """

    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]

    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_imgs.append(bb_img)

    return bb_imgs, bb_accs

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

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    移動量のタプルと対応するこうかとん画像Surfaceの辞書を返す関数
    戻り値: {(横移動量, 縦移動量): 画像Surface}
    """
    # ベースのこうかとん画像（3.png）
    base_img = pg.image.load("fig/3.png")

    # 反転させて「右向き」を基準にする
    right_img = pg.transform.flip(base_img, True, False)

    kk_dict = {
        (0, 0): pg.transform.rotozoom(base_img, 0, 0.9),       # スタート
        (-5, 0): pg.transform.rotozoom(base_img, 0, 0.9),      # 左
        (-5, -5): pg.transform.rotozoom(base_img, -45, 0.9),   # 左上
        (0, -5): pg.transform.rotozoom(right_img, 90, 0.9),    # 上
        (+5, -5): pg.transform.rotozoom(right_img, 45, 0.9),   # 右上
        (+5, 0): pg.transform.rotozoom(right_img, 0, 0.9),     # 右
        (+5, +5): pg.transform.rotozoom(right_img, -45, 0.9),  # 右下
        (0, +5): pg.transform.rotozoom(right_img, -90, 0.9),   # 下
        (-5, +5): pg.transform.rotozoom(base_img, 45, 0.9),    # 左下
    }
    return kk_dict

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

    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]  # 最初は1番小さな爆弾
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5

    kk_imgs = get_kk_imgs()

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
        
        kk_rct.move_ip(sum_mv)

        # 【練習3：こうかとんが画面外に出ないようにする】
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 動く前の位置に戻す

        # === 【練習2・3：爆弾の移動と壁反射】 ===
        avx = vx * bb_accs[min(tmr // 500, 9)]
        avy = vy * bb_accs[min(tmr // 500, 9)]
        bb_img = bb_imgs[min(tmr // 500, 9)]

        # 飛ぶ方向に従って画像を切り替える
        kk_img = kk_imgs[tuple(sum_mv)]

        # widthとheightの更新
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向に出そうになったら
            vx *= -1  # 横の移動速度を反転
        if not tate:  # 縦方向に出そうになったら
            vy *= -1  # 縦の移動速度を反転
        screen.blit(bb_img, bb_rct)  # 爆弾を画面に描画
        # ======================================

        # === 【練習4：こうかとんと爆弾の衝突判定】 ===
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
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
