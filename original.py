import pygame as pg
import random as r

# 初期設定
scale_factor = 2
chip_s = int(24*scale_factor) # マップチップ基本サイズ
map_s  = pg.Vector2(16,9)     # マップの横・縦の配置数

# PlayerCharacterクラスの定義
class PlayerCharacter:
  # コンストラクタ
  def __init__(self,name,init_pos,img_path):
    self.pos  = pg.Vector2(init_pos)
    self.size = pg.Vector2(24,32)*scale_factor
    self.dir  = 2
    self.name = name
    img_raw = pg.image.load(img_path)
    self.__img_arr = []
    for i in range(4):
        self.__img_arr.append([])
        for j in range(3):
            p = pg.Vector2(24*j,32*i)
            tmp = img_raw.subsurface(pg.Rect(p,(24,32)))
            tmp = pg.transform.scale(tmp, self.size)
            self.__img_arr[i].append(tmp)
        self.__img_arr[i].append(self.__img_arr[i][1])

    # 移動アニメーション関連
    self.is_moving = False  # 移動処理中は True になるフラグ
    self.__moving_vec = pg.Vector2(0,0) # 移動方向ベクトル
    self.__moving_acc = pg.Vector2(0,0) # 移動微量の累積

  def turn_to(self,dir):
    self.dir = dir

  def move_to(self,vec):
    self.is_moving = True
    self.__moving_vec = vec.copy()
    self.__moving_acc = pg.Vector2(0,0)
    self.update_move_process()
  
  def update_move_process(self):
    assert self.is_moving
    self.__moving_acc += self.__moving_vec * 3
    if self.__moving_acc.length() >= chip_s:
      self.pos += self.__moving_vec
      self.is_moving = False

  def get_dp(self):
    dp = self.pos*chip_s - pg.Vector2(0,12)*scale_factor
    if self.is_moving :  # キャラ状態が「移動中」なら
      dp += self.__moving_acc # 移動微量の累積値を加算
    return dp
  
  def get_img(self,frame):
    return self.__img_arr[self.dir][frame//6%4]

# ゲームループを含むメイン処理
def main():
    pg.init()
    pg.display.set_caption('草原で遊ぼう')
    map_s  = pg.Vector2(16,9)
    disp_w = int(chip_s*map_s.x)
    disp_h = int(chip_s*map_s.y)
    screen = pg.display.set_mode((disp_w,disp_h))
    clock  = pg.time.Clock()
    font   = pg.font.Font(None,15)
    frame  = 0
    exit_flag = False
    exit_code = '000'
    collision = False
    color=['#ff0000','#0000ff','#00ff00']
    # ボールの描画と位置計算
    ball_p = pg.Vector2(r.randint(0,768), r.randint(0,360)) # x=50, y=90 (px)
    ball_v = pg.Vector2(r.randint(1,3),r.randint(1,3))
    ball_r = r.randint(12,24) # ボールの半径
    ball_c = pg.Color(f'{color[r.randint(0,2)]}')
    ground_img = pg.image.load(f'data/img/map-ground-center.png')
    ground_s   = pg.Vector2(48,48)
    plate_img =pg.image.load(f'data/img/plate.png')
    plate_s=pg.Vector2(48,48)

    # キャラ移動関連
    cmd_move = []
    cmd_move_km = []
    m_vec = [
        pg.Vector2(0,-1),  # 0: 上移動 
        pg.Vector2(1,0),   # 1: 右移動
        pg.Vector2(0,1),   # 2: 下移動
        pg.Vector2(-1,0)   # 3: 左移動
    ] 
    
    # キャラの生成・初期化
    char_arr = []
    char_arr.append(PlayerCharacter('reimu',(3,4),'./data/img/reimu.png'))
    char_arr.append(PlayerCharacter('marisa',(12,4),'./data/img/marisa.png'))
    for _ in char_arr:
        cmd_move.append(-1)
        cmd_move_km.append([])
    
    # 各キャラの移動キーの設定 上・右・下・左
    cmd_move_km[0]=[pg.K_w,pg.K_d,pg.K_s,pg.K_a]
    cmd_move_km[1]=[pg.K_UP,pg.K_RIGHT,pg.K_DOWN,pg.K_LEFT]
    # ゲームループ
    while not exit_flag:
        # システムイベントの検出
        for event in pg.event.get():
            if event.type == pg.QUIT: # ウィンドウ[X]の押下
                exit_flag = True
                exit_code = '001'
                    
        # キー状態の取得 と 各キャラの移動コマンドcmd_moveの更新
        key = pg.key.get_pressed()
        for p in range(len(char_arr)):
            cmd_move[p] = -1
            for i, k in enumerate(cmd_move_km[p]):
                cmd_move[p] = i if key[k] else cmd_move[p]
        # 背景描画
        screen.fill(pg.Color('WHITE'))
        for x in range(0,disp_w,int(plate_s.x)):
            for y in range(0,disp_h,int(plate_s.y)):
                screen.blit(plate_img,(x,y-48))
        for x in range(0,disp_w,int(ground_s.x)):
            screen.blit(ground_img,(x,disp_h-ground_s.y))
        
        pg.draw.circle(screen,ball_c,ball_p,ball_r,)
        ball_p += ball_v
        
        ## 上下との衝突処理
        if ball_p.y >= disp_h - ground_s.y - ball_r :
          ball_p.y = disp_h - ground_s.y - ball_r
          ball_v.y = - 0.8 * ball_v.y
        elif ball_p.y - ball_r < 0:
          ball_p.y = ball_r
          ball_v.y = -0.8 * ball_v.y

        ## 右端と左端との衝突
        if ball_p.x + ball_r > disp_w :
          ball_p.x = disp_w - ball_r
          ball_v.x = -0.8 * ball_v.x 
        elif ball_p.x - ball_r < 0:
          ball_p.x = ball_r
          ball_v.x = -0.8 * ball_v.x
        # 各キャラの移動コマンドの処理
        for p, char in enumerate(char_arr):
            if not char.is_moving :
                if cmd_move[p] != -1:
                    char.turn_to(cmd_move[p])
                    af_pos = char.pos + m_vec[cmd_move[p]] # 移動(仮)した座標
                    # 衝突検出
                    for other_char in char_arr:
                        if other_char != char and other_char.pos == af_pos:
                            collision = True
                            break
                    # 衝突があった場合、または画面範囲外の場合は移動しない
                    if (0 <= af_pos.x <= map_s.x-1) and (0 <= af_pos.y <= map_s.y-2):
                        for other_char in char_arr:
                            if other_char != char and other_char.pos == af_pos:
                                collision = True
                                break
                        # 衝突がなければ移動
                        if not collision:
                            char.move_to(m_vec[cmd_move[p]]) # 画面範囲内なら移動指示
                        else:
                        # 衝突があった場合、他の方向に移動
                            for i in range(4): # 4方向を試す
                              new_dir = (cmd_move[p] + i) % 4
                              new_pos = char.pos + m_vec[new_dir]
                              if (0 <= new_pos.x <= map_s.x-1) and (0 <= new_pos.y <= map_s.y-1) :
                                collision = False
                                for other_char in char_arr:
                                  if other_char != char and other_char.pos == new_pos:
                                    collision = True
                                    break
                                if not collision:
                                  char.turn_to(new_dir)
                                  char.move_to(m_vec[new_dir]) # 他の方向に移動
                                  break
            # キャラが移動中ならば、移動アニメ処理の更新
            if char.is_moving:
                char.update_move_process()
            # キャラの描画
            screen.blit(char.get_img(frame), char.get_dp())
        
        # フレームカウンタ と 各キャラのグリッド座標 の描画
        frame += 1
        frm_str = f'{frame:05}'
        screen.blit(font.render(frm_str,True,'BLACK'),(10,10))
        for p, char in enumerate(char_arr):
            info = f'{char.name} = {char.pos}'
            screen.blit(font.render(info,True,'BLACK'),(10,20+10*p))
        
        # 画面の更新と同期
        pg.display.update()
        clock.tick(30)
    # ゲームループ終了
    pg.quit()
    return exit_code

if __name__ == "__main__":
  code = main()
  print(f'プログラムを「コード{code}」で終了しました。')