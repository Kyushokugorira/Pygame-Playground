import pygame as pg

pg.init() 
pg.display.set_caption('ぼくのかんがえたさいきょうのげーむ II')
screen = pg.display.set_mode((768,432))
clock  = pg.time.Clock()
frame  = 0
exit_flag = False
exit_code = '000'

# 自キャラ移動関連
cmd_move = -1 # 移動コマンドの管理変数

# 自キャラの画像読込み
reimu_p_x = 2  # 自キャラのグリッド座標 X
reimu_p_y = 3  # 自キャラのグリッド座標 Y
reimu_d = 2    # 自キャラの向き
reimu_img_raw = pg.image.load('./data/img/reimu.png')

reimu_img_arr = []

# 上方向のキャラクタアニメーション
reimu_img_arr.append([])
img = reimu_img_raw.subsurface(pg.Rect((0,0), (24, 32)))
reimu_img_arr[0].append(pg.transform.scale(img, (48, 64)))
img = reimu_img_raw.subsurface(pg.Rect((24,0), (24, 32)))
reimu_img_arr[0].append(pg.transform.scale(img, (48, 64)))
img = reimu_img_raw.subsurface(pg.Rect((48,0), (24, 32)))
reimu_img_arr[0].append(pg.transform.scale(img, (48, 64)))
img = reimu_img_raw.subsurface(pg.Rect((24,0), (24, 32)))
reimu_img_arr[0].append(pg.transform.scale(img, (48, 64)))

# 右方向のキャラクタアニメーション
reimu_img_arr.append([])
img = reimu_img_raw.subsurface(pg.Rect((0,32), (24, 32)))
reimu_img_arr[1].append(pg.transform.scale(img, (48, 64)))
img = reimu_img_raw.subsurface(pg.Rect((24,32), (24, 32)))
reimu_img_arr[1].append(pg.transform.scale(img, (48, 64)))
img = reimu_img_raw.subsurface(pg.Rect((48,32), (24, 32)))
reimu_img_arr[1].append(pg.transform.scale(img, (48, 64)))
img = reimu_img_raw.subsurface(pg.Rect((24,32), (24, 32)))
reimu_img_arr[1].append(pg.transform.scale(img, (48, 64)))

# 下方向のキャラクタアニメーション
reimu_img_arr.append([])
img = reimu_img_raw.subsurface(pg.Rect((0,64), (24, 32)))
reimu_img_arr[2].append(pg.transform.scale(img, (48, 64)))
img = reimu_img_raw.subsurface(pg.Rect((24,64), (24, 32)))
reimu_img_arr[2].append(pg.transform.scale(img, (48, 64)))
img = reimu_img_raw.subsurface(pg.Rect((48,64), (24, 32)))
reimu_img_arr[2].append(pg.transform.scale(img, (48, 64)))
img = reimu_img_raw.subsurface(pg.Rect((24,64), (24, 32)))
reimu_img_arr[2].append(pg.transform.scale(img, (48, 64)))

# 左方向のキャラクタアニメーション
reimu_img_arr.append([])
img = reimu_img_raw.subsurface(pg.Rect((0,96), (24, 32)))
reimu_img_arr[3].append(pg.transform.scale(img, (48, 64)))
img = reimu_img_raw.subsurface(pg.Rect((24,96), (24, 32)))
reimu_img_arr[3].append(pg.transform.scale(img, (48, 64)))
img = reimu_img_raw.subsurface(pg.Rect((48,96), (24, 32)))
reimu_img_arr[3].append(pg.transform.scale(img, (48, 64)))
img = reimu_img_raw.subsurface(pg.Rect((24,96), (24, 32)))
reimu_img_arr[3].append(pg.transform.scale(img, (48, 64)))

# ゲームループ
while not exit_flag:

  # システムイベントの検出
  cmd_move = -1
  for event in pg.event.get():
    if event.type == pg.QUIT: # ウィンドウ[X]の押下
      exit_flag = True
      exit_code = '001'
    # 移動操作の「キー入力」の受け取り処理
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_UP:
        cmd_move = 0
      elif event.key == pg.K_RIGHT:
        cmd_move = 1
      elif event.key == pg.K_DOWN:
        cmd_move = 2
      elif event.key == pg.K_LEFT:
        cmd_move = 3

  # 背景描画
  screen.fill(pg.Color('WHITE'))

  # グリッド
  pg.draw.line(screen,'#bbbbbb',(0,0),(0,432))
  pg.draw.line(screen,'#bbbbbb',(48,0),(48,432))
  pg.draw.line(screen,'#bbbbbb',(96,0),(96,432))
  pg.draw.line(screen,'#bbbbbb',(144,0),(144,432))
  pg.draw.line(screen,'#bbbbbb',(192,0),(192,432))
  pg.draw.line(screen,'#bbbbbb',(240,0),(240,432))
  pg.draw.line(screen,'#bbbbbb',(288,0),(288,432))
  pg.draw.line(screen,'#bbbbbb',(336,0),(336,432))
  pg.draw.line(screen,'#bbbbbb',(384,0),(384,432))
  pg.draw.line(screen,'#bbbbbb',(432,0),(432,432))
  pg.draw.line(screen,'#bbbbbb',(480,0),(480,432))
  pg.draw.line(screen,'#bbbbbb',(528,0),(528,432))
  pg.draw.line(screen,'#bbbbbb',(576,0),(576,432))
  pg.draw.line(screen,'#bbbbbb',(624,0),(624,432))
  pg.draw.line(screen,'#bbbbbb',(672,0),(672,432))
  pg.draw.line(screen,'#bbbbbb',(720,0),(720,432))

  pg.draw.line(screen,'#bbbbbb',(0,0),(768,0))
  pg.draw.line(screen,'#bbbbbb',(0,48),(768,48))
  pg.draw.line(screen,'#bbbbbb',(0,96),(768,96))
  pg.draw.line(screen,'#bbbbbb',(0,144),(768,144))
  pg.draw.line(screen,'#bbbbbb',(0,192),(768,192))
  pg.draw.line(screen,'#bbbbbb',(0,240),(768,240))
  pg.draw.line(screen,'#bbbbbb',(0,288),(768,288))
  pg.draw.line(screen,'#bbbbbb',(0,336),(768,336))
  pg.draw.line(screen,'#bbbbbb',(0,384),(768,384))

  # 移動コマンドの処理
  if cmd_move != -1:
    reimu_d = cmd_move
    af_pos_x = reimu_p_x
    af_pos_y = reimu_p_y
    if cmd_move == 0:
      af_pos_y = reimu_p_y - 1
    elif cmd_move == 1:
      af_pos_x = reimu_p_x + 1
    elif cmd_move == 2:
      af_pos_y = reimu_p_y + 1
    elif cmd_move == 3:
      af_pos_x = reimu_p_x - 1
      
    if 0 <= af_pos_x :
      if af_pos_x <= 15:
        if 0 <= af_pos_y : 
          if af_pos_y <= 8 :
            if cmd_move == 0:
              reimu_p_y = reimu_p_y - 1
            elif cmd_move == 1:
              reimu_p_x = reimu_p_x + 1
            elif cmd_move == 2:
              reimu_p_y = reimu_p_y + 1
            elif cmd_move == 3:
              reimu_p_x = reimu_p_x - 1

  # 自キャラの描画
  af = frame//6%4
  screen.blit(reimu_img_arr[reimu_d][af],(reimu_p_x*48,reimu_p_y*48-24))

  # フレームカウンタの描画
  frame = frame + 1
  screen.blit(pg.font.Font(None,15).render(f'{frame:05}',True,'BLACK'),(10,10))
  screen.blit(pg.font.Font(None,15).render(f'[{reimu_p_x},{reimu_p_y}]',True,'BLACK'),(10,20))
  
  # 画面の更新と同期
  pg.display.update()
  clock.tick(30)
# ゲームループ [ここまで]

pg.quit()
print(f'プログラムを「コード{exit_code}」で終了しました。')