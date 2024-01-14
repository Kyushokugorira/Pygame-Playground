import pygame as pg

def main():

  # 初期化処理
  pg.init() 
  pg.display.set_caption('ぼくのかんがえたさいきょうのげーむ')
  disp_w, disp_h = 800, 600
  screen = pg.display.set_mode((disp_w,disp_h)) # WindowSize
  clock  = pg.time.Clock()
  font   = pg.font.Font(None,15)
  frame  = 0
  exit_flag = False
  exit_code = '000'

  # ボールのパラメータ p:位置、v:速度、a:加速度
  ball_p = pg.Vector2(50, 90)  # x=50, y=90 (px)
  ball_v = pg.Vector2(2, 0)    # vx=2, vy=0 (px/frm)
  ball_a = pg.Vector2(0, 0.9)  # ax=0, ay=0.9 (px/frm^2)
  ball_r = 24                  # ボールの半径
  ball_c = pg.Color('#ff0000') # ボールの色

  ground_h = 48 # 地面の高さ

  # ゲームループ
  while not exit_flag:

    # システムイベントの検出
    for event in pg.event.get():
      if event.type == pg.QUIT: # ウィンドウ[X]の押下
        exit_flag = True
        exit_code = '001'

    # 背景描画
    screen.fill(pg.Color('WHITE'))

    # ボールの描画、位置・速度の更新
    pg.draw.circle(screen,ball_c,ball_p,ball_r)
    ball_p += ball_v
    ball_v += ball_a

    ## 地面との衝突処理
    if ball_p.y >= disp_h - ground_h - ball_r :
      ball_p.y = disp_h - ground_h - ball_r
      ball_v.y = - 0.8 * ball_v.y

    ## 右端と左端との衝突処理
    if ball_p.x + ball_r > disp_w :
      ball_p.x = disp_w - ball_r
      ball_v.x = -0.8 * ball_v.x 
    elif ball_p.x - ball_r < 0:
      ball_p.x = ball_r
      ball_v.x = -0.8 * ball_v.x 

    # 地面描画 rectの 第3引数は (左上X, 左上Y ,幅 ,高さ)
    pg.draw.rect(screen, pg.Color('#864A2B'),
                (0, disp_h-ground_h, disp_w, disp_h))

    # フレームカウンタの描画
    frame += 1
    frm_str = f'{frame:05}'
    screen.blit(font.render(frm_str,True,'BLACK'),(10,10))

    # 画面の更新と同期
    pg.display.update()
    clock.tick(30)

  # ゲームループ [ここまで]
  pg.quit()
  return exit_code

if __name__ == "__main__":
  code = main()
  print(f'プログラムを「コード{code}」で終了しました。')