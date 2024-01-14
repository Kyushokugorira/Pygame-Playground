import random as r
import pygame as pg

def main():

  # 初期化処理
  pg.init() 
  pg.display.set_caption('ぼくのかんがえたさいきょうのげーむ')
  disp_w, disp_h = 800, 600
  screen = pg.display.set_mode((disp_w,disp_h))
  clock  = pg.time.Clock()
  font   = pg.font.Font(None,15)
  frame  = 0
  exit_flag = False
  exit_code = '000'

  face_s = pg.Vector2(48,48) # サイズ
  face_r = face_s/2          # 半径
  face_p = pg.Vector2(50,90) # 位置
  face_v = pg.Vector2(2,0)   # 速度
  face_a = pg.Vector2(0,0.2) # 加速度
  face_img = pg.image.load(f'data/img/marisa-face.png')

  ground_img = pg.image.load(f'data/img/map-ground-center.png')
  ground_s   = pg.Vector2(48,48) 

  jump = False  # ジャンプアクション入力の有無
  theta = 0.0   # 顔の回転角 (deg) を保持する変数

  # 炎エフェクト
  fire_img = pg.image.load(f'data/img/effect-fire.png')
  fire_img = pg.transform.rotozoom(fire_img,180,1) # 180度の回転
  fire = 0   # 炎を表示する残り時間を保持する変数

  # 敵(死神関係)
  enemy_img = pg.image.load(f'data/img/shinigami.png')
  enemy_s   = pg.Vector2(48,48)
  enemy_p_arr = [
    pg.Vector2(200,150),
    pg.Vector2(400,200),
    pg.Vector2(600,100),
  ]
  enemy_rect_arr = []  # 衝突判定用の矩形(くけい)
  for enemy_p in enemy_p_arr:
    enemy_rect_arr.append(pg.Rect(enemy_p,enemy_s)) 

  damage = 0 # 敵に衝突直後の無敵時間の残りを保持する変数

  # ゲームループ
  while not exit_flag:

    # システムイベントの検出
    for event in pg.event.get():
      if event.type == pg.QUIT:
        exit_flag = True
        exit_code = '001'
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_SPACE:
          jump = True
          fire = 6  # 6フレーム間、炎を表示

    # 敵との接触判定
    if damage == 0:
      # 魔理沙の現在位置をあらわす矩形を設定
      face_rect = pg.Rect((face_p-face_s/2),face_s)
      for enemy_rect in enemy_rect_arr:
        if enemy_rect.colliderect(face_rect): # 衝突判定
          damage = 20  # これがゼロになるまで無敵
          break
    else:
      damage -= 1  # 無敵時間の残りをデクリメント

    # 背景描画
    if damage == 0:
      screen.fill(pg.Color('#48c0f0'))
    else :
      screen.fill(pg.Color('#ff0000'))

    # 敵の描画
    for enemy_p in enemy_p_arr:
      screen.blit(enemy_img,enemy_p)

    # 火のエフェクト処理
    if fire > 0 :
      tmp_p = face_p - pg.Vector2(24,r.randint(-10,0))
      screen.blit(fire_img,tmp_p)
      fire -= 1

    # ジャンプアクション処理
    if jump:
      face_v.y = -8
      face_v.y = -8
      face_v.x += 0.5 if face_v.x > 0 else  -0.5
      jump = False
    
    # 魔理沙の回転角度の計算
    if face_v.x > 0 : 
      theta -= min(20,face_v.magnitude_squared()*2.4)
    else :
      theta += min(20,face_v.magnitude_squared()*2.4)

    # 魔理沙の描画
    img = pg.transform.rotozoom(face_img,theta,1) # imgを回転
    tmp_p = face_p - (img.get_rect().center) # 描画開始位置(左上)の計算
    screen.blit(img,tmp_p)

    # 位置と速度の更新
    face_p += face_v
    face_v += face_a

    ## 地面との衝突処理
    if face_p.y >= disp_h - ground_s.y - face_r.y :
      face_p.y = disp_h - ground_s.y - face_r.y
      face_v.y = - 0.7 * ( face_v.y - face_a.y )
      if abs(face_v.y) < 3.5 :
        face_v.y = 0
        face_v.x *= 0.98  

    ## 右端と左端との衝突
    if face_p.x + face_r.x > disp_w :
      face_p.x = disp_w - face_r.x
      face_v.x = -0.8 * face_v.x 
    elif face_p.x - face_r.x < 0:
      face_p.x = face_r.x
      face_v.x = -0.8 * face_v.x 

    # 地面描画
    for x in range(0,disp_w,int(ground_s.x)):
      screen.blit(ground_img,(x,disp_h-ground_s.y))

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