#import "AppDelegate.h"
#import "DeskViewController.h"

@implementation AppDelegate

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    self.window = [[UIWindow alloc] initWithFrame:[UIScreen mainScreen].bounds];
    DeskViewController *desk = [[DeskViewController alloc] init];
    UINavigationController *nav = [[UINavigationController alloc] initWithRootViewController:desk];
    self.window.rootViewController = nav;
    [self.window makeKeyAndVisible];
    return YES;
}

@end
