import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.ArrayList;
import java.util.Random;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.Timer;
import javax.swing.JOptionPane;

/**
 * FlappyBirdGame - A simple Flappy Bird clone implemented using Java Swing.
 * This class handles the main window and contains the game logic panel.
 */
public class FlappyBirdGame {

    // --- MAIN METHOD ---
    public static void main(String[] args) {
        // Create the main window frame
        JFrame frame = new JFrame("Flappy Bird in Java");
        
        // Create and add the game panel
        GamePanel gamePanel = new GamePanel();
        frame.add(gamePanel);
        
        // Setup frame properties
        frame.pack(); // Size the frame to fit the panel
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setResizable(false);
        frame.setLocationRelativeTo(null); // Center the window
        frame.setVisible(true);

        // Start the game loop managed by the Timer in the GamePanel
        gamePanel.startGame();
    }

    // --- BIRD CLASS ---
    static class Bird {
        public int x, y; // Position
        public final int SIZE = 40; // Diameter of the bird
        public double velocity;
        public final double GRAVITY = 0.5;
        public final double JUMP_STRENGTH = -9.0;

        public Bird(int x, int y) {
            this.x = x;
            this.y = y;
            this.velocity = 0;
        }

        public void update() {
            // Apply gravity to velocity
            velocity += GRAVITY;
            // Update vertical position
            y += velocity;
            
            // Simple velocity damping (optional, makes it smoother)
            velocity *= 0.98;
        }

        public void jump() {
            velocity = JUMP_STRENGTH;
        }

        public void draw(Graphics g) {
            // Draw Bird Body (Yellow Circle)
            g.setColor(new Color(252, 211, 77)); // Tailwind Yellow-400
            g.fillOval(x, y, SIZE, SIZE);
            
            // Draw Outline
            g.setColor(new Color(146, 64, 14)); // Dark Brown
            g.drawOval(x, y, SIZE, SIZE);

            // Draw Eye (Small black circle)
            g.setColor(Color.BLACK);
            g.fillOval(x + (int)(SIZE * 0.7), y + (int)(SIZE * 0.2), SIZE / 6, SIZE / 6);
        }
    }

    // --- PIPE CLASS ---
    static class Pipe {
        public int x; // Horizontal position
        public final int WIDTH = 60;
        public int gapY; // Center Y position of the gap
        public final int GAP_HEIGHT = 160;
        public final int SPEED = 3;
        public boolean scored = false;

        public Pipe(int x, int gapY) {
            this.x = x;
            this.gapY = gapY;
        }

        public void update() {
            x -= SPEED; // Move pipes to the left
        }

        public void draw(Graphics g, int height) {
            g.setColor(new Color(16, 185, 129)); // Tailwind Emerald-500 (Pipe Color)
            
            // Draw Top Pipe
            int topPipeHeight = gapY - GAP_HEIGHT / 2;
            g.fillRect(x, 0, WIDTH, topPipeHeight);

            // Draw Bottom Pipe
            int bottomPipeY = gapY + GAP_HEIGHT / 2;
            int bottomPipeHeight = height - bottomPipeY;
            g.fillRect(x, bottomPipeY, WIDTH, bottomPipeHeight);

            // Add Darker borders for detail
            g.setColor(new Color(4, 120, 87)); // Darker Emerald
            g.drawRect(x, 0, WIDTH, topPipeHeight);
            g.drawRect(x, bottomPipeY, WIDTH, bottomPipeHeight);
        }
    }

    // --- GAME PANEL (Handles drawing and logic) ---
    static class GamePanel extends JPanel implements ActionListener, KeyListener {
        
        // Game Dimensions
        private final int GAME_WIDTH = 480;
        private final int GAME_HEIGHT = 720;
        
        // Game Objects
        private Bird bird;
        private ArrayList<Pipe> pipes;
        private Timer timer;
        private Random random;

        // Game State
        private boolean isRunning = false;
        private int score;
        private long lastPipeTime;
        private final long PIPE_INTERVAL = 1500; // milliseconds

        // UI elements
        private final int GROUND_HEIGHT = 30;
        private Font scoreFont = new Font("Arial", Font.BOLD, 48);

        public GamePanel() {
            setPreferredSize(new Dimension(GAME_WIDTH, GAME_HEIGHT));
            setBackground(new Color(125, 211, 252)); // Tailwind Sky-300 (Sky background)
            setFocusable(true); // Allows key events to be captured
            addKeyListener(this);
            
            random = new Random();
            resetGame();
            
            // Setup the game loop timer (e.g., 60 frames per second)
            timer = new Timer(1000 / 60, this);
        }
        
        // Initialization/Reset function
        private void resetGame() {
            bird = new Bird(GAME_WIDTH / 4, GAME_HEIGHT / 2, 0);
            pipes = new ArrayList<>();
            score = 0;
            isRunning = false;
        }

        public void startGame() {
            isRunning = true;
            lastPipeTime = System.currentTimeMillis();
            timer.start();
        }

        // Timer event handling (the core game loop)
        @Override
        public void actionPerformed(ActionEvent e) {
            if (isRunning) {
                updateGame();
                repaint(); // Calls paintComponent
            }
        }

        // Game logic update
        private void updateGame() {
            bird.update();
            
            // Check for pipe spawning
            long currentTime = System.currentTimeMillis();
            if (currentTime - lastPipeTime > PIPE_INTERVAL) {
                spawnPipe();
                lastPipeTime = currentTime;
            }

            // Update and check pipes
            for (int i = 0; i < pipes.size(); i++) {
                Pipe pipe = pipes.get(i);
                pipe.update();

                // Check for scoring
                // If the pipe passed the bird's center (x + half size) and hasn't been scored
                if (!pipe.scored && pipe.x + pipe.WIDTH < bird.x + bird.SIZE / 2) {
                    score++;
                    pipe.scored = true;
                }

                // Check collision
                if (checkCollision(pipe)) {
                    gameOver();
                    return; // Stop processing after game over
                }
            }

            // Remove off-screen pipes
            pipes.removeIf(pipe -> pipe.x + pipe.WIDTH < 0);
            
            // Check ground/ceiling collision
            if (bird.y + bird.SIZE > GAME_HEIGHT - GROUND_HEIGHT || bird.y < 0) {
                gameOver();
            }
        }
        
        private void spawnPipe() {
            // Random Y for gap center, between 25% and 75% of game height (excluding ground)
            int minGapY = (int) (GAME_HEIGHT * 0.25);
            int maxGapY = (int) (GAME_HEIGHT * 0.75) - GROUND_HEIGHT;
            int gapY = random.nextInt(maxGapY - minGapY) + minGapY;

            pipes.add(new Pipe(GAME_WIDTH, gapY));
        }

        private boolean checkCollision(Pipe pipe) {
            // Check if bird's bounding box overlaps pipe's horizontal position
            if (bird.x + bird.SIZE > pipe.x && bird.x < pipe.x + pipe.WIDTH) {
                // Top pipe collision
                int topPipeBottom = pipe.gapY - pipe.GAP_HEIGHT / 2;
                if (bird.y < topPipeBottom) {
                    return true;
                }
                
                // Bottom pipe collision
                int bottomPipeTop = pipe.gapY + pipe.GAP_HEIGHT / 2;
                if (bird.y + bird.SIZE > bottomPipeTop) {
                    return true;
                }
            }
            return false;
        }

        private void gameOver() {
            isRunning = false;
            timer.stop();
            repaint(); // Draw the final state
            
            // Use a standard Swing dialog for Game Over message
            JOptionPane.showMessageDialog(this, 
                "Game Over! Your Score: " + score + "\nPress ENTER or click 'OK' to restart.", 
                "Game Over", 
                JOptionPane.INFORMATION_MESSAGE);
            
            resetGame(); // Prepare for the next game
            startGame(); // Automatically restart
        }
        
        // --- RENDERING ---
        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g); // Draws the background
            
            // Draw Pipes
            for (Pipe pipe : pipes) {
                pipe.draw(g, GAME_HEIGHT);
            }
            
            // Draw Bird
            bird.draw(g);

            // Draw Ground
            g.setColor(new Color(76, 175, 80)); // Tailwind Green-600
            g.fillRect(0, GAME_HEIGHT - GROUND_HEIGHT, GAME_WIDTH, GROUND_HEIGHT);
            g.setColor(new Color(27, 94, 32)); // Darker Green border
            g.drawLine(0, GAME_HEIGHT - GROUND_HEIGHT, GAME_WIDTH, GAME_HEIGHT - GROUND_HEIGHT);

            // Draw Score
            g.setColor(Color.WHITE);
            g.setFont(scoreFont);
            String scoreStr = String.valueOf(score);
            int strWidth = g.getFontMetrics().stringWidth(scoreStr);
            g.drawString(scoreStr, (GAME_WIDTH - strWidth) / 2, 60);

            // Draw Start/Pause message if not running
            if (!isRunning) {
                 g.setColor(new Color(255, 255, 255, 180)); // Semi-transparent white
                 g.setFont(new Font("Arial", Font.BOLD, 30));
                 String startMsg = "Press SPACE to jump!";
                 int msgWidth = g.getFontMetrics().stringWidth(startMsg);
                 g.drawString(startMsg, (GAME_WIDTH - msgWidth) / 2, GAME_HEIGHT / 3);
            }
        }

        // --- KEY LISTENER INTERFACE METHODS ---
        @Override
        public void keyPressed(KeyEvent e) {
            if (e.getKeyCode() == KeyEvent.VK_SPACE || e.getKeyCode() == KeyEvent.VK_UP) {
                if (isRunning) {
                    bird.jump();
                } else {
                    startGame(); // Start game on first spacebar press
                }
            }
        }

        // Unused methods required by KeyListener interface
        @Override
        public void keyTyped(KeyEvent e) {}

        @Override
        public void keyReleased(KeyEvent e) {}
    }
}
